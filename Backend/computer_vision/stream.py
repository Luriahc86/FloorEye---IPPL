import cv2
import os
import time


def _is_file(path):
    try:
        return os.path.isfile(path)
    except Exception:
        return False


def get_rtsp_stream(rtsp_url, reopen_delay: float = 2.0):
    """Buka RTSP stream atau file video dan yield frame.

    - Jika path adalah file dan mencapai EOF, akan me-rewind ke frame awal dan lanjutkan.
    - Jika gagal membaca frame, akan menunggu sebentar dan mencoba lagi (untuk RTSP).
    - Mencoba membuka dengan backend FFMPEG jika tersedia.
    """
    print(f"[INFO] Opening stream/video: {rtsp_url}")

    # jika path file, cek keberadaan
    if _is_file(rtsp_url):
        if not os.path.exists(rtsp_url):
            raise Exception(f"File tidak ditemukan: {rtsp_url}")

    # coba beberapa opsi membuka VideoCapture
    cap = None
    try:
        # prefer FFMPEG backend when tersedia
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        if cap is None or not cap.isOpened():
            cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            raise Exception("Gagal membuka stream/video dengan VideoCapture")

        # print some info for debugging
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print(f"[INFO] Video opened. FPS={fps}, FrameCount={frame_count}")

        while True:
            ret, frame = cap.read()

            if not ret:
                # jika file, kemungkinan EOF -> rewind
                if _is_file(rtsp_url):
                    print("[INFO] EOF reached for video file, rewinding to start.")
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    time.sleep(0.1)
                    continue
                # jika stream RTSP, coba tunggu dan coba lagi
                print("[WARNING] Gagal membaca frame dari stream, retrying...")
                time.sleep(reopen_delay)
                # apabila stream benar-benar closed, coba re-open
                if not cap.isOpened():
                    try:
                        cap.release()
                    except Exception:
                        pass
                    try:
                        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
                    except Exception:
                        cap = cv2.VideoCapture(rtsp_url)
                continue

            yield frame

    except Exception as e:
        raise
    finally:
        try:
            if cap is not None:
                cap.release()
        except Exception:
            pass
