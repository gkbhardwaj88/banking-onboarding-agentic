import re
PAN_REGEX = r"[A-Z]{5}[0-9]{4}[A-Z]"

def parse_pan(text: str):
    txt = text or ""
    pan = re.search(PAN_REGEX, txt.replace(" ", ""))
    pan_num = pan.group(0) if pan else None
    name = ""; father = ""; dob = None
    if "Name:" in txt:
        seg = txt.split("Name:")[1]
        name = seg.split("Father")[0].replace(":", "").strip().title()
    if "Father" in txt:
        father = txt.split("Father")[-1].replace(":", "").strip().title()
    m = re.search(r"\d{2}/\d{2}/\d{4}", txt)
    if m: dob = m.group(0)
    return {"pan": pan_num, "name": name, "father_name": father, "dob": dob}
