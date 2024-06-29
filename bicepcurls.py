import cv2
import mediapipe as mp
import numpy as np
import csv
import datetime

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize counters and stages for both arms
left_counter = 0
right_counter = 0
left_stage = None
right_stage = None

#============Calculate Angles============================================================
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

cap = cv2.VideoCapture(0)

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    frame_count = 0  # Add a frame count variable
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1  # Increment frame count

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks for the left arm
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for the left arm
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate angle for the left arm
            left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

            # Visualize angle for the left arm
            cv2.putText(image, f"Left Angle: {left_angle}",
                        tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw lines on the left arm for better visualization
            cv2.line(image, tuple(np.multiply(left_shoulder, [640, 480]).astype(int)),
                     tuple(np.multiply(left_elbow, [640, 480]).astype(int)), (255, 0, 0), 2)
            cv2.line(image, tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                     tuple(np.multiply(left_wrist, [640, 480]).astype(int)), (255, 0, 0), 2)

            # Curl counter logic for the left arm
            if left_angle > 160:
                left_stage = "down"
            if left_angle < 30 and left_stage == 'down':
                left_stage = "up"
                left_counter += 1
                print("Left Reps:", left_counter)
                winsound.Beep(1000, 200)  # Beep sound for feedback

        except:
            pass

        # Extract landmarks for the right arm
        try:
           
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate angle for the right arm
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            # Visualize angle for the right arm
            cv2.putText(image, f"Right Angle: {right_angle}",
                        tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw lines on the right arm for better visualization
            cv2.line(image, tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                     tuple(np.multiply(right_elbow, [640, 480]).astype(int)), (255, 0, 0), 2)
            cv2.line(image, tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                     tuple(np.multiply(right_wrist, [640, 480]).astype(int)), (255, 0, 0), 2)

            # Curl counter logic for the right arm
            if right_angle > 160:
                right_stage = "down"
            if right_angle < 30 and right_stage == 'down':
                right_stage = "up"
                right_counter += 1
                print("Right Reps:", right_counter)
                winsound.Beep(1000, 200)  # Beep sound for feedback

                # Save repetition data to a CSV file
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('repetition_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Right', timestamp, right_angle])

        except:
            pass

        # Render curl counters for both arms
        cv2.putText(image, 'Left Reps: ' + str(left_counter),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        cv2.putText(image, 'Right Reps: ' + str(right_counter),
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)

        cv2.imshow('BicepCurls Screen', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
