import cv2 as cv
import numpy as np
import mediapipe as mp
from utils import recognizer
from vidgear.gears import CamGear



# Initialize MediaPipe Hands model
recognizer = recognizer.recognizer()

stream = False

word = input("put the path of vedio, or just word 'camera':")
if word == "camera":
    try:
        c = cv.VideoCapture(0, cv.CAP_AVFOUNDATION) # Capture the default camera
    except:
        print("Default Camera is currently invalid")
elif word[0:6] == 'https:':
    c = CamGear(source='https://youtu.be/942WxIbXupw', stream_mode = True, logging=True).start()
    stream = True
else:
    try:
        c = cv.VideoCapture(word)
    except:
        print("invalid path")

while True:
    # Capture each frame within the camera
    if stream:
        frame = c.read()
    else:
        ret, frame = c.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

    # Convert the frame to RGB for hand detection
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    # The detector is initialized. Use it here.
    gesture_recognition_result = recognizer.recognize(mp_rgb_frame)
    if gesture_recognition_result.gestures and gesture_recognition_result.gestures[0]:
        
        posture = gesture_recognition_result.gestures[0][0].category_name
        cv.putText(frame, posture, (100,100), cv.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3, cv.LINE_AA)

        handness = gesture_recognition_result.handedness[0][0].category_name
        cv.putText(frame, handness, (300,100), cv.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 255), 3, cv.LINE_AA)

        # Draw landmarks on the frame(green dots) 
        for landmarks in gesture_recognition_result.hand_landmarks[0]:
            x, y = int(landmarks.x * frame.shape[1]), int(landmarks.y * frame.shape[0])
            cv.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # Display the frame with imshow.
    cv.imshow("Camera Feed", frame)



# Stop the images showing after q pressed:
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
    
# Release camera and close all opencv windows.
if stream:
    c.stop()
else:
    c.release()
cv.destroyAllWindows()
