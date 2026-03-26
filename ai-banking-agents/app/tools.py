import os
import requests
import uuid

SUREPASS_TOKEN = os.getenv("SUREPASS_TOKEN")


def ocr_pan(pan_bytes: bytes | None):
    # placeholder OCR; real implementation would call EasyOCR/Tesseract
    return {"fallback_text": "", "parsed": {}}


def validate_aadhaar(id_number: str):
    if not SUREPASS_TOKEN:
        return {"error": "missing_token"}
    headers = {"Authorization": f"Bearer {SUREPASS_TOKEN}", "Content-Type": "application/json"}
    resp = requests.post("https://sandbox.surepass.io/api/v1/aadhaar-validation/aadhaar-validation", json={"id_number": id_number}, headers=headers)
    return resp.json()


def generate_otp(id_number: str):
    headers = {"Authorization": f"Bearer {SUREPASS_TOKEN}", "Content-Type": "application/json"}
    resp = requests.post("https://sandbox.surepass.io/api/v1/aadhaar-v2/generate-otp", json={"id_number": id_number}, headers=headers)
    return resp.json()


def submit_otp(client_id: str, otp: str):
    headers = {"Authorization": f"Bearer {SUREPASS_TOKEN}", "Content-Type": "application/json"}
    resp = requests.post("https://sandbox.surepass.io/api/v1/aadhaar-v2/submit-otp", json={"client_id": client_id, "otp": otp}, headers=headers)
    return resp.json()


def create_payment_order(amount_paise: int, currency: str = "INR"):
    return {
        "order_id": f"order_{uuid.uuid4().hex[:14]}",
        "amount": amount_paise,
        "currency": currency,
        "status": "created",
    }
