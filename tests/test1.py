from eyeGestures.utils import VideoCapture
from eyeGestures.eyegestures import EyeGestures_v2
#from eyeGestures import Camera
import eyeGestures as eg
import cv2

# Initialize gesture engine and video capture
gestures = EyeGestures_v2()
cap = VideoCapture("http://127.0.0.1:5696/video") # 5

#camera = Camera()

calibrate = True
screen_width = 1280
screen_height= 960

# Process each frame
while True:
    ret, frame = cap.read()
    """ event, cevent = gestures.step(frame,
        calibrate,
        screen_width,
        screen_height,
        context="my_context")
    print(ret)
    print(frame)
    if event:
        cursor_x, cursor_y = event.point[0], event.point[1]
        fixation = event.fixation
        # calibration_radius: radius for data collection during calibration """
    
    cv2.imshow('Camera', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    """ #==============
    frame = camera.get_frame()
    gestures = eg.detect_gestures(frame)

    # Interpret the gestures
    for gesture in gestures:
        if gesture == eg.LEFT_WINK:
            print("Left wink detected!")
        elif gesture == eg.RIGHT_WINK:
            print("Right wink detected!")
        # Add more gesture handling as needed """

cap.close()
cv2.destroyAllWindows()
#camera.release()