import cv2
import mediapipe as mp
import math
import os

# ======= SETTINGS =======
IMAGE_PATH = ""  # Change this to your image path
START_SCALE = 0.3   # Start zoomed out (0.3 = 30% of original size)
START_X = 0.7       # X position (0 = left, 1 = right)
START_Y = 0.1       # Y position (0 = top, 1 = bottom)
# ========================

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"Image not found at: {IMAGE_PATH}")

image = cv2.imread(IMAGE_PATH)
image_h, image_w = image.shape[:2]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
