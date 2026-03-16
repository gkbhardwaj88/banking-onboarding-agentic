import os
import cv2
import dlib
from scipy.spatial import distance

# Resolve predictor path relative to this file to avoid cwd issues
PREDICTOR_PATH = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")

detector = dlib.get_frontal_face_detector()
try:
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
except RuntimeError:
    predictor = None  # Handle missing model file gracefully

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def detect_blink(frame):
    if predictor is None:
        # Model file missing; skip blink detection
        return False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        shape = predictor(gray, face)
        left_eye = [(shape.part(i).x, shape.part(i).y) for i in range(36, 42)]
        ear = eye_aspect_ratio(left_eye)
        if ear < 0.2:
            return True
    return False
