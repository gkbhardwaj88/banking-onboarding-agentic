from backend.aadhaar.qr_decoder import decode_qr
from backend.aadhaar.xml_parser import parse_aadhaar_xml

def process_aadhaar(image_bytes: bytes):
    qr_text = decode_qr(image_bytes)
    if qr_text:
        try:
            return parse_aadhaar_xml(qr_text)
        except:
            pass
    return {"error": "Failed to parse Aadhaar QR/XML"}
