import requests, re
from ..config import SUREPASS_TOKEN

HEAD = lambda: {"Authorization": f"Bearer {SUREPASS_TOKEN}", "Content-Type": "application/json"}

def validate(id_number: str):
    if not SUREPASS_TOKEN:
        return {"error":"missing_token"}
    r = requests.post("https://sandbox.surepass.io/api/v1/aadhaar-validation/aadhaar-validation",
                      json={"id_number": id_number}, headers=HEAD(), timeout=10)
    return r.json()

def generate_otp(id_number: str):
    r = requests.post("https://sandbox.surepass.io/api/v1/aadhaar-v2/generate-otp",
                      json={"id_number": id_number}, headers=HEAD(), timeout=10)
    return r.json()

def submit_otp(client_id: str, otp: str):
    r = requests.post("https://sandbox.surepass.io/api/v1/aadhaar-v2/submit-otp",
                      json={"client_id": client_id, "otp": otp}, headers=HEAD(), timeout=10)
    return r.json()

def parse_aadhaar_text(text: str):
    txt = text or ""
    dob = re.search(r"\d{2}/\d{2}/\d{4}", txt)
    dob = dob.group(0) if dob else None
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    name = ""
    for i,l in enumerate(lines):
        if "government of india" in l.lower() and i+1 < len(lines):
            name = re.sub(r"[^A-Za-z ]","", lines[i+1]).title()
            break
    aadhaar_num = re.search(r"[2-9]\d{11}", re.sub(r"\D","", txt))
    aadhaar_num = aadhaar_num.group(0) if aadhaar_num else None
    return {"name": name, "dob": dob, "aadhaar_number": aadhaar_num}
