import cv2
import dlib

detector = dlib.get_frontal_face_detector()

def detect_head_movement(prev_frame, curr_frame):
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(prev_gray, curr_gray)
    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    movement = cv2.countNonZero(thresh)
    return movement > 5000
