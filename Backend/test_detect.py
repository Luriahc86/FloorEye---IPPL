import cv2
import os
import sys

from computer_vision.detector import detect_dirty_floor

img_path = 'assets/test_kotor.png'
if len(sys.argv) > 1:
    img_path = sys.argv[1]

if not os.path.exists(img_path):
    print('[ERROR] Image not found:', img_path)
    sys.exit(1)

img = cv2.imread(img_path)
if img is None:
    print('[ERROR] Failed to read image (cv2.imread returned None)')
    sys.exit(1)

print('[INFO] Image loaded:', img_path)

print('[INFO] Running detect_dirty_floor with debug=True and conf_threshold=0.2')
detected = detect_dirty_floor(img, conf_threshold=0.2, debug=True)

print('[RESULT] Dirty floor detected:', detected)
