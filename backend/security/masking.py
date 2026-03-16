def mask_aadhaar(num: str):
    return "XXXX XXXX " + num[-4:]

def mask_pan(pan: str):
    return pan[:3] + "XX" + pan[-3:]
