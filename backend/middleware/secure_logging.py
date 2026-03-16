import logging

SENSITIVE_KEYS = ["aadhaar", "pan", "password"]

def secure_log(msg: dict):
    scrubbed = {k: ("***" if k in SENSITIVE_KEYS else v) for k,v in msg.items()}
    logging.info(scrubbed)
