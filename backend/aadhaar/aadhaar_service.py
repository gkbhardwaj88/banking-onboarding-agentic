from backend.aadhaar.qr_decoder import decode_qr
from backend.aadhaar.xml_parser import parse_aadhaar_xml
from backend.aadhaar import surepass_client

def process_aadhaar(image_bytes: bytes):
    qr_text = decode_qr(image_bytes)
    if qr_text:
        try:
            return parse_aadhaar_xml(qr_text)
        except:
            pass
    return {"error": "Failed to parse Aadhaar QR/XML"}


def validate_aadhaar_number(id_number: str, token: str | None = None):
    """
    Validate Aadhaar number via Surepass sandbox (fallback when QR parsing fails).
    """
    try:
        return surepass_client.validate_aadhaar(id_number, token=token)
    except Exception as exc:
        return {"error": "aadhaar_validation_failed", "details": str(exc)}


def generate_aadhaar_otp(id_number: str, token: str | None = None):
    try:
        return surepass_client.generate_otp(id_number, token=token)
    except Exception as exc:
        return {"error": "otp_generation_failed", "details": str(exc)}


def submit_aadhaar_otp(client_id: str, otp: str, token: str | None = None):
    try:
        return surepass_client.submit_otp(client_id, otp, token=token)
    except Exception as exc:
        return {"error": "otp_submit_failed", "details": str(exc)}
