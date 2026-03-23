import re

PAN_REGEX = r'^[A-Z]{5}[0-9]{4}[A-Z]$'

def extract_pan_fields(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    pan = None
    name = None
    father = None
    dob = None

    for ln in lines:
        token = ln.replace(" ", "")
        if re.match(PAN_REGEX, token):
            pan = token
        if "Father" in ln or "FATHER" in ln:
            father = ln.replace("Father's Name", "").strip().replace("Father Name", "")
        if "Name" in ln and "Father" not in ln:
            name = ln.replace("Name", "").strip()
        if re.search(r'\d{2}/\d{2}/\d{4}', ln):
            dob = re.search(r'\d{2}/\d{2}/\d{4}', ln).group()

    return {
        "pan": pan,
        "name": name,
        "father_name": father,
        "dob": dob
    }

def validate_pan(pan: str):
    return bool(re.match(PAN_REGEX, pan))
