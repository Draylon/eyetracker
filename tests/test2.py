import cv2
import dlib

# Initialize webcam
cap = cv2.VideoCapture(7,cv2.CAP_DSHOW)

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # Ensure this file is downloaded

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        # Extract eye coordinates (landmark points for eyes are 36-41 for the left eye and 42-47 for the right eye)
        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]

        # Draw circles on eyes
        for point in left_eye + right_eye:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

    cv2.imshow("Eye Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()