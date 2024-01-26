import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Exercise counter variables
counter_pushups = 0
counter_situps = 0
counter_squats = 0
counter_bicep_curls = 0
stage_pushups = None
stage_situps = None
stage_squats = None
stage_bicep_curls = None

# Constants
ANGLE_THRESHOLD_DOWN = 160
ANGLE_THRESHOLD_UP = 30

# Function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Exercise counting logic
def count_pushups(angle, stage_var):
    global counter_pushups
    if angle > ANGLE_THRESHOLD_DOWN and stage_var != 'down':
        stage_var = 'down'
    elif angle < ANGLE_THRESHOLD_UP and stage_var == 'down':
        stage_var = 'up'
        counter_pushups += 1
        print(f"Push-ups: {counter_pushups}")
    return stage_var

def count_situps(angle, stage_var):
    global counter_situps
    if angle > ANGLE_THRESHOLD_DOWN and stage_var != 'down':
        stage_var = 'down'
    elif angle < ANGLE_THRESHOLD_UP and stage_var == 'down':
        stage_var = 'up'
        counter_situps += 1
        print(f"Sit-ups: {counter_situps}")
    return stage_var

def count_squats(angle, stage_var):
    global counter_squats
    if angle > ANGLE_THRESHOLD_DOWN and stage_var != 'down':
        stage_var = 'down'
    elif angle < ANGLE_THRESHOLD_UP and stage_var == 'down':
        stage_var = 'up'
        counter_squats += 1
        print(f"Squats: {counter_squats}")
    return stage_var

def count_bicep_curls(angle, stage_var):
    global counter_bicep_curls
    if angle > ANGLE_THRESHOLD_DOWN and stage_var != 'down':
        stage_var = 'down'
    elif angle < ANGLE_THRESHOLD_UP and stage_var == 'down':
        stage_var = 'up'
        counter_bicep_curls += 1
        print(f"Bicep Curls: {counter_bicep_curls}")
    return stage_var

# Exercise selection callback
def select_exercise(event):
    global selected_exercise
    selected_exercise = exercise_var.get()

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    cap = cv2.VideoCapture(0)

    # Create the GUI window
    root = tk.Tk()
    root.title("Exercise Tracker")

    # Heading label
    heading_label = tk.Label(root, text="Exercise Tracker", font=("Helvetica", 20), padx=10, pady=10)
    heading_label.grid(row=0, column=0, columnspan=3)

    # Dropdown menu for exercise selection
    exercise_var = tk.StringVar(root)
    exercise_var.set("Push-ups")  # Default exercise
    exercises = ["Push-ups", "Sit-ups", "Squats", "Bicep Curls"]
    exercise_menu = ttk.Combobox(root, textvariable=exercise_var, values=exercises, font=("Helvetica", 14))
    exercise_menu.grid(row=1, column=0, padx=10, pady=10, sticky="W")
    exercise_menu.bind("<<ComboboxSelected>>", select_exercise)

    # Initialize selected_exercise
    selected_exercise = exercise_var.get()

    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Calculate angles based on selected exercise
            if selected_exercise == "Push-ups":
                angle = calculate_angle(shoulder, elbow, wrist)
                stage_pushups = count_pushups(angle, stage_pushups)
            elif selected_exercise == "Sit-ups":
                angle = calculate_angle(hip, knee, ankle)
                stage_situps = count_situps(angle, stage_situps)
            elif selected_exercise == "Squats":
                angle = calculate_angle(hip, knee, ankle)
                stage_squats = count_squats(angle, stage_squats)
            elif selected_exercise == "Bicep Curls":
                angle = calculate_angle(shoulder, elbow, wrist)
                stage_bicep_curls = count_bicep_curls(angle, stage_bicep_curls)
            else:
                angle = 0

        except Exception as e:
            print(e)

        # Render exercise counter
        if selected_exercise == "Push-ups":
            counter_var = counter_pushups
            stage_var = stage_pushups
        elif selected_exercise == "Sit-ups":
            counter_var = counter_situps
            stage_var = stage_situps
        elif selected_exercise == "Squats":
            counter_var = counter_squats
            stage_var = stage_squats
        elif selected_exercise == "Bicep Curls":
            counter_var = counter_bicep_curls
            stage_var = stage_bicep_curls
        else:
            counter_var = 0
            stage_var = None

        # Render exercise counter
        counter_label = tk.Label(root, text=f'{selected_exercise}: {counter_var}', font=("Helvetica", 16), padx=10, pady=10)
        counter_label.grid(row=2, column=0, columnspan=3)

        # Render pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        # Display video feed
        cv2.imshow('Exercise Tracker', image)

        # Update the Tkinter window
        root.update()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    root.destroy()
