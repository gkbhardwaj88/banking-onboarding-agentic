import xml.etree.ElementTree as ET
import base64

def parse_aadhaar_xml(xml_str: str):
    root = ET.fromstring(xml_str)
    data = {
        "name": root.attrib.get("name"),
        "dob": root.attrib.get("dob"),
        "gender": root.attrib.get("gender"),
        "aadhaar_last4": root.attrib.get("uid")[-4:] if root.attrib.get("uid") else None,
        "address": {},
        "photo": None
    }

    addr = root.find("Poa")
    if addr is not None:
        for k,v in addr.attrib.items():
            data["address"][k] = v

    photo_node = root.find("Pht")
    if photo_node is not None:
        data["photo"] = photo_node.text

    return data
