from djitellopy import Tello
import cv2
import time
import numpy as np

# Initialize the Tello drone
tello = Tello()
tello.connect()
tello.streamon()

# Load the Haar Cascade for upper body detection from file
person_cascade = cv2.CascadeClassifier('cascades\haarcascade_upperbody.xml')

# Parameters
FRAME_WIDTH, FRAME_HEIGHT = 640, 480  # Resolution of the drone's video feed
desired_distance_pixels = 160         # Calibrate to match 1.5 meters
center_x_threshold = 40               # Tolerance for center alignment
max_speed = 50     ''                   # Max drone speed (0-100)

# Variables to track previous position and time
prev_position = None
prev_time = None
movement_detected = False

# Create a map for displaying the walking route
map_size = 800  # Size of the map window
map_image = np.ones((map_size, map_size, 3), dtype=np.uint8) * 255  # White background
map_scale = 0.2  # Scaling factor to fit the movement into the map view

# Initial positions for the drone and the person
drone_position = np.array([map_size // 2, map_size // 2])
person_position = np.array([map_size // 2, map_size // 2])

tello.takeoff()
initial_vertical_speed = 30  # Adjust as needed to reach double height
tello.send_rc_control(0, 0, initial_vertical_speed, 0)  # Initial lift-off to desired height

time.sleep(2)

try:
    # Takeoff and hover
    #tello.takeoff()
    #initial_vertical_speed = 20
    #tello.send_rc_control(0, 0, initial_vertical_speed, 0)  # Hover in place
    #time.sleep(2)

    while True:
        # Get the current frame from the Tello camera
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect people in the frame
        people = person_cascade.detectMultiScale(gray, 1.1, 4)

        if len(people) > 0:
            # Assume the largest detection is the person
            x, y, w, h = max(people, key=lambda b: b[2] * b[3])
            person_width_pixels = w
            person_center_x = x + w // 2
            person_center_y = y + h // 2

            # Draw rectangle around detected person
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (person_center_x, person_center_y), 5, (0, 0, 255), -1)

            # Calculate distance and lateral error from the person
            distance_error = desired_distance_pixels - person_width_pixels
            center_offset = person_center_x - FRAME_WIDTH // 2

            # Calculate drone speed adjustments
            forward_speed = int(np.clip(distance_error * 0.5, -max_speed, max_speed))
            lateral_speed = int(np.clip(center_offset * 0.2, -max_speed, max_speed))

            # Determine if the person has stopped
            if prev_position:
                movement_detected = abs(person_center_x - prev_position[0]) > 10 or abs(person_width_pixels - prev_position[1]) > 10
            prev_position = (person_center_x, person_width_pixels)
            prev_time = time.time()

            # Update drone and person position on the map
            delta_x = -lateral_speed * map_scale
            delta_y = -forward_speed * map_scale
            person_position += np.array([delta_x, delta_y], dtype=np.int32)
            drone_position += np.array([delta_x, delta_y], dtype=np.int32)  # Drone follows person

            # Draw the person's path and mark the drone
            cv2.circle(map_image, tuple(person_position), 3, (255, 0, 0), -1)  # Person's path in blue
            cv2.circle(map_image, tuple(drone_position), 5, (0, 0, 255), -1)  # Drone position in red

            # Control the drone
            if abs(distance_error) > 10 or abs(center_offset) > center_x_threshold:
                # Move to keep the distance and center alignment
                tello.send_rc_control(lateral_speed, +forward_speed, 0, 0)
            elif not movement_detected:
                # If no significant movement, hover
                tello.send_rc_control(0, 0, 0, 0)
            else:
                # Move laterally to re-center if the person is moving left/right
                tello.send_rc_control(lateral_speed, 0, 0, 0)

        else:
            # If no person detected, hover in place to avoid unnecessary movements
            tello.send_rc_control(0, 0, 0, 0)

        # Display the frame
        cv2.imshow('Tello Tracking', frame)

        # Display the map with the drone and person's path
        cv2.imshow('Walking Route Map', map_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    # Clean up
    tello.send_rc_control(0, 0, 0, 0)
    tello.land()
    tello.streamoff()
    cv2.destroyAllWindows()
