from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ================= COMPUTER VISION ==================
#from computer_vision.stream import get_rtsp_stream
from computer_vision.detector import detect_dirty_floor
#from computer_vision.notifier import send_notification

# =================== ROUTES =========================
#from routes.auth_route import router as auth_router
#from routes.staff_route import router as staff_router
#from routes.cctv_route import router as cctv_router
#from routes.laporan_route import router as laporan_router
#from routes.profile_route import router as profile_router

# ================== DATABASE =========================
#from database import Base, engine  # NOTE: get_db pindah ke database.py
#from models import User, Staff, CCTV, Laporan

# ======================================================
import threading
import time
import cv2
import os
from contextlib import asynccontextmanager
import sys


# ======================================================
# AUTO CREATE TABLES
# ======================================================
#Base.metadata.create_all(bind=engine)


# ======================================================
# CONFIG
# ======================================================

if 'linux' in sys.platform or os.environ.get('DISPLAY') is None:
    cv2.setUseOptimized(True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RTSP_URL = os.path.join(BASE_DIR, "assets", "test_video.mp4")

PHONE_TARGET = "+6281234567890"  # TODO: ganti nomor WhatsApp penerima
last_notification_time = 0
NOTIFY_INTERVAL = 60  # detik


# ======================================================
# COMPUTER VISION LOOP
# ======================================================

def monitor_floor():
    global last_notification_time
    print("[INFO] Memulai pemantauan stream/video...")

    display_enabled = os.environ.get('DISPLAY') is not None and 'linux' not in sys.platform

    try:
        for frame in get_rtsp_stream(RTSP_URL):
            try:
                detected = detect_dirty_floor(frame, debug=False)

                if display_enabled:
                    try:
                        cv2.imshow("FloorEye Detection", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    except:
                        display_enabled = False

                if detected:
                    now = time.time()
                    if now - last_notification_time > NOTIFY_INTERVAL:
                        try:
                            send_notification(
                                PHONE_TARGET,
                                "🚨 Lantai kotor terdeteksi! Segera bersihkan area tersebut."
                            )
                            print("[ALERT] Notifikasi dikirim.")
                            last_notification_time = now
                        except Exception as e:
                            print("[WARNING] Gagal kirim notifikasi:", e)

            except Exception as e:
                print(f"[ERROR] Kesalahan deteksi: {e}")
                time.sleep(2)
                continue

    except Exception as e:
        print(f"[ERROR] Stream error: {e}")

    finally:
        try:
            cv2.destroyAllWindows()
        except:
            pass


# ======================================================
# LIFESPAN FASTAPI
# ======================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Menjalankan thread Computer Vision...")
    print(f"[INFO] Source video: {RTSP_URL}")

    thread = threading.Thread(target=monitor_floor, daemon=True)
    thread.start()

    yield

    print("[INFO] Server dimatikan. Cleaning up...")
    try:
        cv2.destroyAllWindows()
    except:
        pass


# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI(
    title="FloorEye Backend",
    version="1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTES
#app.include_router(auth_router)
#app.include_router(staff_router)
#app.include_router(cctv_router)
#app.include_router(laporan_router)
#app.include_router(profile_router)

@app.get("/")
def root():
    return {"message": "FloorEye backend berjalan 🚀", "status": "ok"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "video_source": RTSP_URL,
        "notification_interval": NOTIFY_INTERVAL
    }


# ======================================================
# RUN (DEV MODE)
# ======================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
