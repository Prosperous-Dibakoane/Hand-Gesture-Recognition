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

cap = cv2.VideoCapture(0)

scale = START_SCALE
x_offset = int(START_X * (640 - int(image_w * scale)))
y_offset = int(START_Y * (480 - int(image_h * scale)))
is_dragging = False
prev_center = None
prev_distance = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1) 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger tips
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            h, w, _ = frame.shape
            index_tip_pos = (int(index_tip.x * w), int(index_tip.y * h))
            thumb_tip_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))