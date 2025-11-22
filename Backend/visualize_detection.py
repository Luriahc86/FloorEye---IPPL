import cv2
import os
import sys
from computer_vision.detector import MODEL_PATH
from ultralytics import YOLO


import argparse

parser = argparse.ArgumentParser(description='Visualize detections with configurable confidence and image size')
parser.add_argument('image', nargs='?', default='computer_vision/assets/sample_frame.jpg')
parser.add_argument('--conf', type=float, default=0.2, help='confidence threshold')
parser.add_argument('--imgsz', type=int, default=640, help='inference image size (e.g. 640, 1280)')
parser.add_argument('--out', default='computer_vision/assets/output_debug.jpg', help='output annotated image path')
args = parser.parse_args()

img_path = args.image
if not os.path.exists(img_path):
    print('[ERROR] Image not found:', img_path)
    sys.exit(1)

out_path = args.out

print('[INFO] Loading model from:', MODEL_PATH)
model = YOLO(MODEL_PATH)

img = cv2.imread(img_path)
if img is None:
    print('[ERROR] Failed to read image')
    sys.exit(1)

# convert to RGB for model, but keep copy for drawing
img_rgb = img[..., ::-1]

print(f"[INFO] Running inference conf={args.conf} imgsz={args.imgsz}")
try:
    # try using imgsz parameter (works on many ultralytics versions)
    res = model(img_rgb, conf=args.conf, imgsz=args.imgsz)
except TypeError:
    # fallback to 'size' parameter name
    res = model(img_rgb, conf=args.conf, size=args.imgsz)

# draw boxes on original BGR image
for r in res:
    boxes = getattr(r, 'boxes', None)
    if boxes is None:
        continue
    # handle tensors or lists
    try:
        xyxy = boxes.xyxy.cpu().numpy()
        cls_list = [int(x) for x in boxes.cls.cpu().numpy()]
        conf_list = [float(x) for x in boxes.conf.cpu().numpy()]
    except Exception:
        try:
            xyxy = boxes.xyxy.tolist()
            cls_list = [int(x) for x in boxes.cls.tolist()]
            conf_list = [float(x) for x in boxes.conf.tolist()]
        except Exception:
            xyxy = []
            cls_list = []
            conf_list = []

    names = getattr(model, 'names', {})
    for i, c in enumerate(cls_list):
        if i >= len(xyxy):
            continue
        x1, y1, x2, y2 = map(int, xyxy[i])
        label = names.get(c, str(c)) if isinstance(names, dict) else str(c)
        conf = conf_list[i] if i < len(conf_list) else 0.0
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f'{label} {conf:.2f}', (x1, max(16, y1-6)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

cv2.imwrite(out_path, img)
print('[INFO] Saved annotated image to:', out_path)
