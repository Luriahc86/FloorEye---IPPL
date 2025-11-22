import cv2
import base64
import sys
import traceback

# Initialize Roboflow Inference API client
API_KEY = "3p9F8fm0kacQSGcr2DFm"
MODEL_ID = "lantai-bersih-atau-kotor/1"

print(f"[INFO] Initializing Roboflow Inference API with model_id={MODEL_ID}")

try:
    CLIENT = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=API_KEY
    )
    print("[INFO] Roboflow API client initialized successfully")
except Exception as e:
    print(f"[WARNING] Failed to initialize Roboflow API client: {e}")
    CLIENT = None


def detect_dirty_floor(frame, conf_threshold: float = 0.25, debug: bool = False) -> bool:
    """Deteksi apakah ada kotoran di lantai pada frame menggunakan Roboflow API.

    - frame: BGR ndarray dari OpenCV
    - conf_threshold: confidence threshold untuk menganggap deteksi valid
    - debug: jika True, akan mencetak info hasil deteksi

    Mengembalikan True jika ditemukan kelas yang mengindikasikan lantai kotor (dirty/kotor).
    """
    if CLIENT is None:
        print("[ERROR] Roboflow API client not initialized")
        return False

    try:
        # Convert BGR frame ke JPEG bytes untuk dikirim ke API
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("[ERROR] Failed to encode frame to JPEG")
            return False

        # Encode to base64 string
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # Send inference request to Roboflow
        if debug:
            print("[DEBUG] Sending frame to Roboflow API...")

        result = CLIENT.infer(image_base64, model_id=MODEL_ID)

        if debug:
            print(f"[DEBUG] API response: {result}")

        # Extract predictions from response
        predictions = result.get("predictions", [])
        
        if debug:
            print(f"[DEBUG] Number of predictions: {len(predictions)}")

        # Check if any prediction has class indicating dirty floor with confidence > threshold
        for pred in predictions:
            class_name = pred.get("class", "").lower()
            confidence = pred.get("confidence", 0.0)

            if debug:
                print(f"[DEBUG] Prediction: class={class_name} confidence={confidence}")

            # Check for dirty/kotor class with sufficient confidence
            if confidence >= conf_threshold:
                if "dirty" in class_name or "kotor" in class_name:
                    if debug:
                        print(f"[DEBUG] Dirty floor detected with confidence {confidence}")
                    return True

        return False

    except Exception as e:
        print(f"[ERROR] detect_dirty_floor error: {e}")
        traceback.print_exc(file=sys.stdout)
        return False
