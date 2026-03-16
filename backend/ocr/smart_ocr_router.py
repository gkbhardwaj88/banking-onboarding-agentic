from backend.ocr.azure_recognizer import azure_ocr
from backend.ocr.tesseract_fallback import tesseract_ocr
from pytesseract.pytesseract import TesseractNotFoundError

def extract_text(image_bytes: bytes):
    try:
        data = azure_ocr(image_bytes)
        if 'documents' in data:
            return data
    except Exception as exc:
        # ignore and fall back
        fallback_error = str(exc)
    else:
        fallback_error = None

    try:
        return {"fallback_text": tesseract_ocr(image_bytes)}
    except TesseractNotFoundError as exc:
        # Provide explicit guidance to the client
        return {
            "error": "OCR failed",
            "details": "Tesseract not installed or not on PATH",
            "hint": "Install Tesseract locally or set TESSERACT_CMD to its full path",
            "azure_error": fallback_error,
        }
    except Exception as exc:
        return {"error": "OCR failed", "details": str(exc), "azure_error": fallback_error}
