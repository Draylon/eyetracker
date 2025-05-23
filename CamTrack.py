import threading

import pandas as pd
import cv2 as cv
import numpy as np
import mediapipe as mp
import utils

import warnings

# left eyes indices
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 

# irises Indices list
LEFT_IRIS = [474,475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]



FACE_3D_MODEL = np.array([
    [0.0, 0.0, 0.0],  # Nose tip
    [0.0, -330.0, -65.0],  # Chin
    [-225.0, 170.0, -135.0],  # Left eye corner
    [225.0, 170.0, -135.0],  # Right eye corner
    [-150.0, -150.0, -125.0],  # Left mouth corner
    [150.0, -150.0, -125.0]  # Right mouth corner
], dtype=np.float32)

# Indices for the facial landmarks
NOSE_TIP = 1
CHIN = 199
LEFT_EYE_CORNER = 33
RIGHT_EYE_CORNER = 263
LEFT_MOUTH_CORNER = 61
RIGHT_MOUTH_CORNER = 291

class CamTrack:
    def __init__(self):
        'Create camera object'
        self.cap = cv.VideoCapture("http://127.0.0.1:5696/video")
        self.mp_face_mesh = mp.solutions.face_mesh
        self._feature_fetch = lambda *args,**kwargs: None
        
        #self.mask1 = mask = np.zeros((800, 600), dtype=np.uint8)

    def set_featureFetch(self,fun):
        'Set the function to be called each available frame in the camera'
        self._feature_fetch = fun

    def start_worker(self):
        self._stop1 = False
        self._mainthread = utils.StoppableThread(target = self.mainloop)
        #self.mainthread = threading.Thread(target = self.mainloop)
        self._mainthread.start()

    def stop_worker(self):
        self._stop1=True
        self._mainthread.stop()
        self._mainthread.join()

    def mainloop(self):
        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            while not self._mainthread.stopped() and not self._stop1:
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = cv.flip(frame, 1)

                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                img_h, img_w = frame.shape[:2]
                with warnings.catch_warnings(action="ignore"):
                    results = face_mesh.process(rgb_frame)
                #mask = np.zeros((img_h, img_w), dtype=np.uint8)

                if results.multi_face_landmarks:
                    # print((results.multi_face_landmarks[0]))

                    # [print(p.x, p.y, p.z ) for p in results.multi_face_landmarks[0].landmark]
                    
                    mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) 
                    for p in results.multi_face_landmarks[0].landmark])


                    ## ===========FACE DIRECTION VECTOR ================
                    # Corresponding 2D image points from the face mesh
                    FACE_2D_POINTS = np.array([
                        mesh_points[NOSE_TIP],          # Nose tip
                        mesh_points[CHIN],              # Chin
                        mesh_points[LEFT_EYE_CORNER],   # Left eye corner
                        mesh_points[RIGHT_EYE_CORNER],  # Right eye corner
                        mesh_points[LEFT_MOUTH_CORNER], # Left mouth corner
                        mesh_points[RIGHT_MOUTH_CORNER] # Right mouth corner
                    ], dtype=np.float32)

                    # Camera matrix (assumes camera is in the center of the image)
                    focal_length = img_w
                    center = (img_w / 2, img_h / 2)
                    camera_matrix = np.array([
                        [focal_length, 0, center[0]],
                        [0, focal_length, center[1]],
                        [0, 0, 1]
                    ], dtype=np.float32)

                    # No lens distortion
                    dist_coeffs = np.zeros((4, 1))

                    # Solve for pose (rotation and translation vectors)
                    success, rotation_vector, translation_vector = cv.solvePnP(FACE_3D_MODEL, FACE_2D_POINTS, camera_matrix, dist_coeffs)
                    
                    # 2D Face center
                    projected_points_2d, _ = cv.projectPoints(FACE_3D_MODEL, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
                    face_center_3d = np.mean(FACE_3D_MODEL, axis=0)
                    face_center_2d, _ = cv.projectPoints(np.array([face_center_3d]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
                    im2Dface_center = tuple(map(int, face_center_2d[0][0]))


                    # 3D face direction vector
                    rotation_matrix, _ = cv.Rodrigues(rotation_vector)
                    forward_vector = np.array([[0], [0], [1]])
                    direction_vector_3d = rotation_matrix.dot(forward_vector)
                    im3Dface_dir = tuple(direction_vector_3d.ravel())

                    
                    #draw face direction vector
                    nose_end_3d = np.array([[0, 0, 1000.0]], dtype=np.float32)
                    nose_end_2d, _ = cv.projectPoints(nose_end_3d, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
                    p1 = (int(FACE_2D_POINTS[0][0]), int(FACE_2D_POINTS[0][1]))
                    p2 = (int(nose_end_2d[0][0][0]), int(nose_end_2d[0][0][1]))
                    #cv.line(mask, p1, p2, (255, 255, 255), 2)

                    #iris position
                    (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                    (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                    center_left = np.array([l_cx, l_cy], dtype=np.int32)
                    center_right = np.array([r_cx, r_cy], dtype=np.int32)
                    
                    diff_left = mesh_points[LEFT_EYE] - center_left
                    diff_right = mesh_points[RIGHT_EYE] - center_right

                    # ==========DRAW EYES==============

                    #print([mesh_points[LEFT_EYE]])

                    # Draw eye
                    #cv.polylines(mask, [mesh_points[LEFT_EYE]], True, (255, 255, 255), 1, cv.LINE_AA)
                    #cv.polylines(mask, [mesh_points[RIGHT_EYE]], True, (255, 255, 255), 1, cv.LINE_AA)

                    #=================================
                    #+==========DRAW IRIS=============
                    #square
                    # cv.polylines(mask, [mesh_points[LEFT_IRIS]], True, (0,255,0), 1, cv.LINE_AA)
                    # cv.polylines(mask, [mesh_points[RIGHT_IRIS]], True, (0,255,0), 1, cv.LINE_AA)

                    #ball
                    #cv.circle(mask, center_left, int(l_radius), (0,255,0), 2, cv.LINE_AA)
                    #cv.circle(mask, center_right, int(r_radius), (0,255,0), 2, cv.LINE_AA)

                    #crosshair
                    #cv.circle(mask, center_left, 1, (255, 255, 255), -1, cv.LINE_AA)
                    #cv.circle(mask, center_right, 1, (255, 255, 255), -1, cv.LINE_AA)

                    # drawing on the mask 
                    #cv.circle(mask, center_left, int(l_radius), (255,255,255), -1, cv.LINE_AA)
                    #cv.circle(mask, center_right, int(r_radius), (255,255,255), -1, cv.LINE_AA)
                    #================================

                    # this runs in a thread
                    # the core will provide the parameters
                    # this thread will provide the loop
                    self._feature_fetch([
                        np.array([list(im2Dface_center)]),
                        np.array([list(im3Dface_dir)]),
                        diff_left,
                        diff_right
                    ])
                    #self.mask1 = mask
                    
                #cv.imshow('Mask', mask)
                #cv.imshow('img', frame)
                #key = cv.waitKey(1)
                #if key == ord('q'):
                    #break

    
    def __del__(self):
        self.cap.release()
        cv.destroyAllWindows()
