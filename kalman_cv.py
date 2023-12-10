import cv2
import numpy as np
import os

# Initialize Kalman filter parameters
dt = 1.0  # time step
kalman = cv2.KalmanFilter(4, 2)  # 4 states (x, y, vx, vy), 2 measurements (x, y)

# Initial state [x, y, vx, vy]
kalman.statePre = np.array([0, 0, 0, 0], dtype=np.float32)

# Transition matrix A
kalman.transitionMatrix = np.array([[1, 0, dt, 0],
                                    [0, 1, 0, dt],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], dtype=np.float32)

# Measurement matrix H
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], dtype=np.float32)

# Process noise covariance Q
kalman.processNoiseCov = 1e-4 * np.eye(4, dtype=np.float32)

# Measurement noise covariance R
kalman.measurementNoiseCov = 1e-1 * np.eye(2, dtype=np.float32)

# Initialize video capture
cap = cv2.VideoCapture('videos/vid3.mp4')
frames_directory = "videos/frames"
box_directory = "videos/box"
edge_directory = "videos/edge"

# Sampling frequency
fps = cap.get(cv2.CAP_PROP_FPS)
sample_frequency = 2  # Hz
sample_interval = int(round(fps / sample_frequency))
frame_count = 0

heights = []


# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame to initialize the tracking
ret, frame = cap.read()

if not ret:
    print("Error: Could not read the first frame.")
    exit()

# Initialize the Kalman filter with the initial position
kalman.statePre[:2] = frame.shape[1] // 2, frame.shape[0] // 2

while True:
    ret, frame = cap.read()

    if not ret:
        break  # Break the loop if the video ends

    frame_count += 1

    # Only process frames at the desired sample rate
    if frame_count % sample_interval != 0:
        continue

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Save the frame
    output_path = os.path.join(frames_directory, f"frame3_{frame_count}.png")
    cv2.imwrite(output_path, frame)

    # Save the edge detection result
    output_path = os.path.join(edge_directory, f"edge3_{frame_count}.png")
    cv2.imwrite(output_path, edges)

    # Check if any contours are found
    if contours:
        # Take the first contour
        contour = max(contours, key=cv2.contourArea)

        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Measure the object based on the bounding box
        measurement = np.array([[x + w / 2], [y + h / 2]], dtype=np.float32)

        # Correct the prediction based on the measurement
        kalman.correct(measurement)

        # Extract the predicted position
        predicted_position = kalman.predict()[:2]

        # Draw the predicted position as a bounding box
        cv2.rectangle(frame, (int(predicted_position[0]) - h // 2, int(predicted_position[1]) - w // 2),
                      (int(predicted_position[0]) + h // 2, int(predicted_position[1]) + w // 2),
                      (0, 255, 0), 2)
        
        output_path = os.path.join(box_directory, f"box3_{frame_count}.png")
        cv2.imwrite(output_path, frame)

        heights.append([h])
        print(h)

    # Display the frame
    cv2.imshow('Object Tracking', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
