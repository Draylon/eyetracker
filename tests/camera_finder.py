import cv2
import dlib

# Initialize webcam



# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # Ensure this file is downloaded
mcap = 100
icap = 0
working=[]
while icap < mcap:
    print("trying",icap)
    try:
        cap = cv2.VideoCapture("http://127.0.0.1:5696/video")#,cv2.CAP_DSHOW)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        working.append(icap)
    except Exception as e:
        print(e)
        icap+=1
        continue
    while True:
        
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
            icap +=1
            break

    cap.release()
    cv2.destroyAllWindows()
print(working)