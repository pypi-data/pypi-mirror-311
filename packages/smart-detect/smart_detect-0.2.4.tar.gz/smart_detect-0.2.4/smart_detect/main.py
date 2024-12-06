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

    # irregular_count = 0
    # normal_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break

    # Convert the frame to RGB for processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

    # Check if pose landmarks are detected
        if results.pose_landmarks:
            # Extract pose landmarks
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for knees and ankles
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Calculate the angles for both knees
            left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # Display the calculated angles on the frame
            cv2.putText(frame, f"Left Knee Angle: {int(left_knee_angle)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Right Knee Angle: {int(right_knee_angle)}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Check for irregular movements
            if (left_knee_angle < 170 or left_knee_angle > 180) or (right_knee_angle < 170 or right_knee_angle > 180):
                irregular_count += 1
                normal_count = 0  # Reset normal count
            else:
                normal_count += 1
                irregular_count = 0  # Reset irregular count

            # Trigger alert if irregular movement persists
            if irregular_count >= irregular_threshold:
                alert_triggered = True
                cv2.putText(frame, "ALERT: Irregular movement detected!", 
                            (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif normal_count >= normal_threshold:
                    alert_triggered = False
                    cv2.putText(frame, "Movement Normal", 
                            (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Draw pose landmarks on the frame
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        else:
            # If no pose is detected, reset counts and indicate tracking loss
            irregular_count = 0
            normal_count = 0
            cv2.putText(frame, "No Pose Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Display the processed video feed
        cv2.imshow('SMART DETECT: Pose and Movement Analysis', frame)

        # Exit the loop when 'enter' is pressed
        key=cv2.waitKey(1)
        if key==32:
            break
    
    cap.release()
    cv2.destroyAllWindows()
