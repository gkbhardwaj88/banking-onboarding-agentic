import io

import cv2
import numpy as np

# Lazy-load EasyOCR so import errors can be handled upstream
_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        import easyocr  # imported lazily to avoid hard dependency if not installed
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def easyocr_ocr(image_bytes: bytes):
    reader = _get_reader()
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Unable to decode image for OCR")

    results = reader.readtext(img, detail=0, paragraph=True)
    text = "\n".join(results) if results else ""
    return {"fallback_text": text, "engine": "easyocr", "raw": results}
