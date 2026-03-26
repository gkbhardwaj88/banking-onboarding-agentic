import json
import time
from typing import Any, Dict

from backend.ocr.smart_ocr_router import extract_text
from backend.pan.pan_service import process_pan
from backend.aadhaar.aadhaar_service import (
    validate_aadhaar_number,
    generate_aadhaar_otp,
    submit_aadhaar_otp,
)
from backend.payment_gateway import create_order_placeholder


def log_event(session_id: str, event: Dict[str, Any]):
    """Append agent events to a lightweight log file."""
    event["ts"] = time.time()
    event["session_id"] = session_id
    with open("backend/agent/agent_events.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def tool_ocr_pan(pan_bytes: bytes):
    txt = extract_text(pan_bytes)
    parsed = process_pan(txt.get("fallback_text", ""))
    return {"ocr_text": txt, "parsed": parsed}


def tool_validate_aadhaar(id_number: str):
    return validate_aadhaar_number(id_number)


def tool_generate_otp(id_number: str):
    return generate_aadhaar_otp(id_number)


def tool_submit_otp(client_id: str, otp: str):
    return submit_aadhaar_otp(client_id, otp)


def tool_payment_order(amount_paise: int, currency: str = "INR"):
    return create_order_placeholder(amount_paise, currency)


def decide_next(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple rule-based agent planner.
    Returns action dict: {action, tool, params, message, confidence}
    """
    if not state:
        return {
            "action": "idle",
            "tool": None,
            "params": {},
            "message": "No state provided.",
            "confidence": 0.1,
        }

    # If no PAN parsed, suggest PAN OCR
    if not state.get("pan_data") or state["pan_data"].get("error"):
        return {
            "action": "ocr_pan",
            "tool": "tool_ocr_pan",
            "params": {},
            "message": "PAN not parsed; run OCR on PAN image.",
            "confidence": 0.7,
        }
    # If Aadhaar not validated and an aadhaar_number present
    aadhaar_number = state.get("aadhaar_data", {}).get("aadhaar_last4")
    if not aadhaar_number and state.get("aadhaar_number"):
        aadhaar_number = state["aadhaar_number"]
    if aadhaar_number and state.get("validation_ok") is False:
        return {
            "action": "validate_aadhaar",
            "tool": "tool_validate_aadhaar",
            "params": {"id_number": aadhaar_number},
            "message": "Validate Aadhaar number via Surepass.",
            "confidence": 0.6,
        }
    # If validation passed, suggest payment order
    if state.get("validation_ok"):
        return {
            "action": "create_payment_order",
            "tool": "tool_payment_order",
            "params": {"amount_paise": 1000 * 100},
            "message": "Validation ok. Create deposit payment order.",
            "confidence": 0.6,
        }
    # Default fallback
    return {
        "action": "idle",
        "tool": None,
        "params": {},
        "message": "No action determined.",
        "confidence": 0.3,
    }
