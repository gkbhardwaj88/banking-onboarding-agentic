import io, easyocr, cv2, numpy as np
reader = easyocr.Reader(['en'], gpu=False)

def pan_ocr(img_bytes: bytes):
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    lines = reader.readtext(img, detail=0, paragraph=True)
    text = "\n".join(lines)
    return {"fallback_text": text, "lines": lines, "engine": "easyocr"}
