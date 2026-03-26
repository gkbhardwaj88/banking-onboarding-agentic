import os
import requests

SUREPASS_TOKEN = os.getenv("SUREPASS_TOKEN")
SUREPASS_TOKEN_LOCAL = os.getenv("SUREPASS_TOKEN_LOCAL")
SUREPASS_PTOKEN = os.getenv("SUREPASS_PTOKEN")

BASE_HEADERS = {"Content-Type": "application/json"}

GENERATE_OTP_URL = "https://sandbox.surepass.io/api/v1/aadhaar-v2/generate-otp"
SUBMIT_OTP_URL = "https://sandbox.surepass.io/api/v1/aadhaar-v2/submit-otp"
VALIDATE_URL = "https://sandbox.surepass.io/api/v1/aadhaar-validation/aadhaar-validation"


def _auth_headers(token: str | None) -> dict:
    if not token:
        raise RuntimeError("Surepass token not configured (set SUREPASS_TOKEN)")
    headers = BASE_HEADERS.copy()
    headers["Authorization"] = f"Bearer {token}"
    return headers


def validate_aadhaar(id_number: str, token: str | None = None) -> dict:
    """
    Validate Aadhaar number via Surepass sandbox.
    """
    headers = _auth_headers(token or SUREPASS_TOKEN)
    resp = requests.post(VALIDATE_URL, json={"id_number": id_number}, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def generate_otp(id_number: str, token: str | None = None) -> dict:
    """
    Trigger Aadhaar OTP via Surepass sandbox.
    """
    headers = _auth_headers(token or SUREPASS_TOKEN)
    resp = requests.post(GENERATE_OTP_URL, json={"id_number": id_number}, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def submit_otp(client_id: str, otp: str, token: str | None = None) -> dict:
    """
    Submit OTP for Aadhaar verification via Surepass sandbox.
    """
    headers = _auth_headers(token or SUREPASS_TOKEN)
    body = {"client_id": client_id, "otp": otp}
    resp = requests.post(SUBMIT_OTP_URL, json=body, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
