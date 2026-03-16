import cv2
import numpy as np
import tempfile

def verify_face(aadhaar_photo_b64: str, selfie_bytes: bytes):
    try:
        from deepface import DeepFace  # Lazy import to avoid hard dependency at startup
    except Exception as e:
        return {"verified": False, "error": f"deepface unavailable: {e}"}

    nparr = np.frombuffer(selfie_bytes, np.uint8)
    selfie = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    with tempfile.NamedTemporaryFile(suffix='.jpg') as f:
        photo_path = f.name
        with open(photo_path, 'wb') as pf:
            pf.write(aadhaar_photo_b64)

        try:
            result = DeepFace.verify(
                img1_path=photo_path,
                img2_path=selfie,
                model_name="VGG-Face",
                enforce_detection=False,
            )
        except Exception as e:
            return {"verified": False, "error": str(e)}

        return result
