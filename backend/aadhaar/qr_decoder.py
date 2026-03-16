import io
import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


def decode_qr(image_bytes: bytes):
    # Prefer OpenCV detector (no external zbar DLL needed)
    if cv2 is not None:
        np_img = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img_cv is not None:
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img_cv)
            if data:
                return data

    # Fallback to pyzbar if available
    try:
        from pyzbar.pyzbar import decode
    except Exception:
        return None

    img = Image.open(io.BytesIO(image_bytes))
    result = decode(img)
    if not result:
        return None
    return result[0].data.decode()
