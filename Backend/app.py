from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from computer_vision.detector import detect_dirty_floor

from contextlib import asynccontextmanager
import os
import sys
import cv2
import numpy as np
import base64
from typing import List, Optional

from store.db import get_connection


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RTSP_URL = os.path.join(BASE_DIR, "assets", "test_video.mp4")

if "linux" in sys.platform or os.environ.get("DISPLAY") is None:
    cv2.setUseOptimized(True)


class CameraFramePayload(BaseModel):
    image_base64: str
    notes: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    source: str
    is_dirty: bool
    confidence: Optional[float] = None
    notes: Optional[str] = None
    created_at: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] FloorEye Backend Started")
    print(f"[INFO] Video Source (test): {RTSP_URL}")
    yield
    print("[INFO] Server Shutdown")


app = FastAPI(
    title="FloorEye Backend",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def decode_image_from_bytes(data: bytes):
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Gagal decode gambar")
    return img


def decode_image_from_base64(b64_string: str) -> bytes:
    if "," in b64_string:
        b64_string = b64_string.split(",", 1)[1]
    return base64.b64decode(b64_string)


def insert_detection_to_db(
    source: str,
    is_dirty: bool,
    image_path: str,
    confidence: float | None = None,
    notes: str | None = None,
) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO floor_events (source, is_dirty, confidence, notes, image_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (source, int(is_dirty), confidence, notes, image_path),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id
    finally:
        conn.close()


@app.get("/")
def root():
    return {"message": "FloorEye backend berjalan 🚀", "status": "ok"}


@app.get("/health")
def health_check():
    try:
        conn = get_connection()
        conn.close()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "healthy",
        "video_source": RTSP_URL,
        "database": db_status,
    }


@app.post("/detect/image")
async def detect_image(
    file: UploadFile = File(...),
    notes: Optional[str] = None,
):
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="File kosong")

        frame = decode_image_from_bytes(file_bytes)
        is_dirty = detect_dirty_floor(frame, debug=False)
        confidence = None

        save_dir = os.path.join(BASE_DIR, "assets", "saved_images")
        os.makedirs(save_dir, exist_ok=True)

        filename = f"upload_{int(cv2.getTickCount())}.jpg"
        file_path = os.path.join(save_dir, filename)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        new_id = insert_detection_to_db(
            source="upload",
            is_dirty=is_dirty,
            image_path=file_path,
            confidence=confidence,
            notes=notes,
        )

        return {
            "id": new_id,
            "source": "upload",
            "is_dirty": is_dirty,
            "confidence": confidence,
            "notes": notes,
            "image_path": file_path,
            "message": "Deteksi dari gambar upload berhasil disimpan",
        }

    except Exception as e:
        print("[ERROR] detect_image:", e)
        raise HTTPException(status_code=500, detail="Gagal memproses gambar")


@app.post("/detect/frame")
async def detect_frame(payload: CameraFramePayload):
    try:
        image_bytes = decode_image_from_base64(payload.image_base64)
        frame = decode_image_from_bytes(image_bytes)

        is_dirty = detect_dirty_floor(frame, debug=False)
        confidence = None

        save_dir = os.path.join(BASE_DIR, "assets", "saved_images")
        os.makedirs(save_dir, exist_ok=True)

        filename = f"camera_{int(cv2.getTickCount())}.jpg"
        file_path = os.path.join(save_dir, filename)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        new_id = insert_detection_to_db(
            source="camera",
            is_dirty=is_dirty,
            image_path=file_path,
            confidence=confidence,
            notes=payload.notes,
        )

        return {
            "id": new_id,
            "source": "camera",
            "is_dirty": is_dirty,
            "confidence": confidence,
            "notes": payload.notes,
            "image_path": file_path,
            "message": "Deteksi dari kamera berhasil disimpan",
        }

    except Exception as e:
        print("[ERROR] detect_frame:", e)
        raise HTTPException(status_code=500, detail="Gagal memproses frame kamera")


@app.get("/history", response_model=List[HistoryItem])
def get_history(limit: int = 50, offset: int = 0):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT id, source, is_dirty, confidence, notes, created_at
            FROM floor_events
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (limit, offset))
        rows = cursor.fetchall()
        cursor.close()

        history = [
            HistoryItem(
                id=row["id"],
                source=row["source"],
                is_dirty=bool(row["is_dirty"]),
                confidence=row.get("confidence"),
                notes=row.get("notes"),
                created_at=row["created_at"].isoformat(),
            )
            for row in rows
        ]

        return history
    finally:
        conn.close()


@app.get("/image/{event_id}")
def get_image(event_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = "SELECT image_path FROM floor_events WHERE id = %s"
        cursor.execute(sql, (event_id,))
        row = cursor.fetchone()
        cursor.close()

        if not row or not row[0]:
            raise HTTPException(status_code=404, detail="Gambar tidak ditemukan")

        file_path = row[0]

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File fisik tidak ditemukan")

        with open(file_path, "rb") as f:
            image_bytes = f.read()

        return Response(content=image_bytes, media_type="image/jpeg")

    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
