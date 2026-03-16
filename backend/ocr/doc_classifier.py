def classify_document(text: str):
    t = text.lower()
    if "income tax" in t or "permanent account" in t:
        return "PAN"
    if "aadhaar" in t or "uidai" in t:
        return "AADHAAR"
    return "UNKNOWN"
