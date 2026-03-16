from backend.pan.parser import extract_pan_fields, validate_pan

def process_pan(text: str):
    fields = extract_pan_fields(text)
    if not fields.get("pan") or not validate_pan(fields["pan"]):
        return {"error": "Invalid PAN number"}
    return fields
