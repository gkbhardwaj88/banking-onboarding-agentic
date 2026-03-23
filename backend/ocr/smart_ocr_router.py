from backend.ocr.azure_recognizer import azure_ocr
from backend.ocr.easyocr_fallback import easyocr_ocr
from backend.ocr.tesseract_fallback import tesseract_ocr
from pytesseract.pytesseract import TesseractNotFoundError

def extract_text(image_bytes: bytes):
    azure_error = None
    easyocr_error = None

    try:
        data = azure_ocr(image_bytes)
        if 'documents' in data:
            return data
    except Exception as exc:
        # ignore and fall back
        azure_error = str(exc)

    try:
        return easyocr_ocr(image_bytes)
    except Exception as exc:
        easyocr_error = str(exc)

    try:
        return {"fallback_text": tesseract_ocr(image_bytes)}
    except TesseractNotFoundError as exc:
        # Provide explicit guidance to the client
        return {
            "error": "OCR failed",
            "details": "Tesseract not installed or not on PATH",
            "hint": "Install Tesseract locally or set TESSERACT_CMD to its full path",
            "azure_error": azure_error,
            "easyocr_error": easyocr_error,
        }
    except Exception as exc:
        return {
            "error": "OCR failed",
            "details": str(exc),
            "azure_error": azure_error,
            "easyocr_error": easyocr_error,
        }
