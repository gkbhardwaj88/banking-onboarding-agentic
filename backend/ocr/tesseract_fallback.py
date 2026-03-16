import io
import os

import pytesseract
from PIL import Image
from pytesseract.pytesseract import TesseractNotFoundError

# Allow overriding tesseract binary path via env (useful on Windows/local dev)
TESSERACT_CMD = os.getenv("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def tesseract_ocr(img_bytes: bytes):
    img = Image.open(io.BytesIO(img_bytes))
    try:
        return pytesseract.image_to_string(img)
    except TesseractNotFoundError as exc:
        # Raise a clearer message that higher layers can surface
        hint = (
            "Tesseract not found. Install it or set TESSERACT_CMD to the full path "
            "(e.g. C:\\\\Program Files\\\\Tesseract-OCR\\\\tesseract.exe on Windows)."
        )
        raise TesseractNotFoundError(hint) from exc
