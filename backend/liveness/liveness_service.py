import cv2
import numpy as np
from backend.liveness.blink_detector import detect_blink
from backend.liveness.movement_detector import detect_head_movement
from backend.liveness.deepface_match import verify_face

def liveness_check(frames: list, aadhaar_photo_b64: str):
    blink_ok = False
    movement_ok = False

    prev_frame = None

    for f in frames:
        frame = cv2.imdecode(np.frombuffer(f, np.uint8), cv2.IMREAD_COLOR)

        if not blink_ok:
            blink_ok = detect_blink(frame)

        if prev_frame is not None and not movement_ok:
            movement_ok = detect_head_movement(prev_frame, frame)

        prev_frame = frame

    face_match = verify_face(aadhaar_photo_b64, frames[-1])

    score = sum([blink_ok, movement_ok, face_match["verified"]])
    return {
        "blink": blink_ok,
        "movement": movement_ok,
        "face_match": face_match["verified"],
        "score": score,
        "passed": score >= 2
    }
