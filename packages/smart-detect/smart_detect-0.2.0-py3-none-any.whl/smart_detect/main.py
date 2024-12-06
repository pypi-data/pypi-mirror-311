import cv2
import mediapipe as mp
from .utils import calculate_angle

def start_tracking(irregular_threshold=15, normal_threshold=15):
    # Initialize Mediapipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    irregular_count = 0
    normal_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # Get joint coordinates and calculate angles here...
            # (Use `calculate_angle` from utils)
            # Add your pose processing logic here
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('SMART DETECT: Pose and Movement Analysis', frame)

        if cv2.waitKey(1) & 0xFF == 32:  # Exit on pressing space
            break

    cap.release()
    cv2.destroyAllWindows()
