import re
import streamlit as st

PAN_REGEX = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
AADHAAR_REGEX = r"^[2-9]\d{11}$"


def _validate_pan(pan: str) -> bool:
    return bool(pan and re.match(PAN_REGEX, pan.strip()))


def _validate_aadhaar(aadhaar: str) -> bool:
    return bool(aadhaar and re.match(AADHAAR_REGEX, aadhaar.strip()))


def _extract_aadhaar_from_text(text: str) -> str:
    if not text:
        return ""
    # Allow spaces between digits (common in Aadhaar print)
    cleaned = re.sub(r"\D", "", text)
    match = re.search(r"[2-9]\d{11}", cleaned)
    return match.group(0) if match else ""


def _extract_pan_from_text(text: str) -> str:
    if not text:
        return ""
    # PAN appears without spaces typically; try all words
    for token in re.findall(r"[A-Z0-9]{8,10}", text):
        if re.match(PAN_REGEX, token):
            return token
    # fallback: return any 10-char alnum token as a weak guess
    for token in re.findall(r"[A-Z0-9]{10}", text):
        return token
    return ""


def _extract_dob(text: str) -> str:
    if not text:
        return ""
    m = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
    if m:
        return m.group(0)
    m = re.search(r"\b\d{4}-\d{2}-\d{2}\b", text)
    return m.group(0) if m else ""


def _extract_name_from_line(line: str) -> str:
    if not line:
        return ""
    # Remove common prefixes
    clean = re.sub(r"(?i)government of india", "", line)
    clean = re.sub(r"(?i)dob[: ]*\d{2}/\d{2}/\d{4}", "", clean)
    clean = re.sub(r"(?i)female|male|transgender", "", clean)
    # Drop numbers and extra symbols
    clean = re.sub(r"[0-9#@:]", "", clean)
    # Collapse spaces
    return " ".join(clean.split()).strip().title()


def _parse_from_fallback(text: str) -> dict:
    """
    Extract best-effort fields from OCR fallback text alone.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    joined = " ".join(lines)

    aadhaar_number = _extract_aadhaar_from_text(text)
    aadhaar_dob = _extract_dob(text)
    aadhaar_name = ""
    aadhaar_address = ""

    # Name: try line after 'Government of India' or first line with DOB
    for i, ln in enumerate(lines):
        if "government of india" in ln.lower():
            candidate = ln
            if i + 1 < len(lines):
                candidate = lines[i + 1]
            aadhaar_name = _extract_name_from_line(candidate)
            break
    if not aadhaar_name and aadhaar_dob:
        # line containing dob
        for ln in lines:
            if aadhaar_dob in ln:
                aadhaar_name = _extract_name_from_line(ln)
                break

    # Address: take the line starting with 'Address' and the next line if present
    for i, ln in enumerate(lines):
        if ln.lower().startswith("address"):
            addr_parts = [ln]
            if i + 1 < len(lines):
                addr_parts.append(lines[i + 1])
            aadhaar_address = " ".join(addr_parts)
            break

    pan_number = _extract_pan_from_text(text)
    pan_dob = _extract_dob(text)
    # PAN name: look for a line with uppercase words before a PAN-like token
    pan_name = ""
    for ln in lines:
        if _extract_pan_from_text(ln):
            # use previous non-empty line as name hint
            idx = lines.index(ln)
            if idx > 0:
                pan_name = _extract_name_from_line(lines[idx - 1])
            break
    if not pan_name:
        pan_name = aadhaar_name  # last resort

    return {
        "aadhaar": {
            "name": aadhaar_name,
            "dob": aadhaar_dob,
            "address": aadhaar_address,
            "aadhaar_number": aadhaar_number,
        },
        "pan": {
            "pan": pan_number,
            "dob": pan_dob,
            "name": pan_name,
        },
    }


def review_form(show_photos: bool = True, advance_step: int = 5, submit_label: str = "Save & Continue"):
    data = st.session_state.get("kyc_data", {})
    payload = data.get("details", data) or {}

    aadhaar_data = payload.get("aadhaar_data") or {}
    pan_data = payload.get("pan_data") or {}
    aadhaar_ocr = payload.get("ocr_text", {}) or {}
    pan_ocr = payload.get("pan_ocr_text", {}) or {}
    ocr_fallback_pan = pan_ocr.get("fallback_text", "") or aadhaar_ocr.get("fallback_text", "")
    ocr_fallback_aadhaar = aadhaar_ocr.get("fallback_text", "")
    ocr_fallback = ocr_fallback_aadhaar or ocr_fallback_pan

    # Status banner
    if data.get("error") or payload.get("validation_ok") is False:
        st.error("KYC rejected – please verify and correct the details below.")
    else:
        st.success("KYC accepted – review and proceed.")

    st.markdown("### Review & Correct Your Details")
    st.caption("We pre-filled these fields from OCR. Please verify, correct if needed, then continue.")

    # Raw JSON for transparency
    with st.expander("Raw KYC JSON (for audit/debug)"):
        st.json(data)

    # Pre-fill form values
    # PAN hints from structured or OCR
    lines = [ln for ln in ocr_fallback_pan.splitlines() if ln.strip()]
    parsed_pan = _parse_from_fallback(ocr_fallback_pan)
    parsed_aadhaar = _parse_from_fallback(ocr_fallback_aadhaar)

    pan_name = pan_data.get("name") or parsed_pan["pan"]["name"] or parsed_aadhaar["aadhaar"]["name"]
    pan_father = pan_data.get("father_name") or ""
    pan_dob = pan_data.get("dob") or parsed_pan["pan"]["dob"] or parsed_aadhaar["aadhaar"]["dob"]
    pan_number = pan_data.get("pan") or parsed_pan["pan"]["pan"] or ""

    # Aadhaar hints
    aadhaar_name = aadhaar_data.get("name") or parsed_aadhaar["aadhaar"]["name"]
    aadhaar_father = aadhaar_data.get("address", {}).get("co") or ""  # care-of often holds father/spouse
    if not aadhaar_father:
        rel_lines = [ln for ln in ocr_fallback.splitlines() if any(k in ln.lower() for k in ["s/o", "d/o", "w/o", "wife of", "son of", "daughter of"])]
        if rel_lines:
            aadhaar_father = " ".join(rel_lines[0].split()[2:]).title() if "wife of" in rel_lines[0].lower() else " ".join(rel_lines[0].split()[1:]).title()
    aadhaar_dob = aadhaar_data.get("dob") or parsed_aadhaar["aadhaar"]["dob"]
    aadhaar_number = aadhaar_data.get("aadhaar_last4") or parsed_aadhaar["aadhaar"]["aadhaar_number"]
    aadhaar_address = ""
    if isinstance(aadhaar_data.get("address"), dict):
        aadhaar_address = ", ".join(aadhaar_data["address"].values())
    if not aadhaar_address:
        # Try to pull from OCR text lines containing 'Address'
        if parsed_aadhaar["aadhaar"]["address"]:
            aadhaar_address = parsed_aadhaar["aadhaar"]["address"]
        else:
            addr_lines = [ln for ln in ocr_fallback_aadhaar.splitlines() if "address" in ln.lower()]
            if addr_lines:
                aadhaar_address = " ".join(addr_lines)

    # Choose a photo to show: Aadhaar -> PAN -> first selfie frame (from liveness step)
    selfie_frames = st.session_state.get("selfie_frames") or payload.get("selfie_frames") or []
    selfie_photo = selfie_frames[0] if selfie_frames else None

    with st.form("kyc_review_form"):
        st.subheader("OCR Snippet")
        st.text_area("OCR Snippet (PAN)", ocr_fallback_pan, height=120, help="OCR used for PAN extraction")
        if show_photos:
            st.text_area("OCR Snippet (Aadhaar)", ocr_fallback_aadhaar, height=80, help="OCR used for Aadhaar extraction")

        # Photo previews if available
        if show_photos:
            photo_col1, photo_col2 = st.columns(2)
            with photo_col1:
                if aadhaar_data.get("photo"):
                    st.image(aadhaar_data["photo"], caption="Aadhaar Photo (base64)", use_column_width=True)
                elif selfie_photo:
                    st.image(selfie_photo, caption="Selfie (used when Aadhaar photo missing)", use_column_width=True)
                else:
                    st.info("Aadhaar photo not available.")
            with photo_col2:
                if pan_data.get("photo"):
                    st.image(pan_data["photo"], caption="PAN Photo", use_column_width=True)
                elif selfie_photo:
                    st.image(selfie_photo, caption="Selfie (used when PAN photo missing)", use_column_width=True)
                else:
                    st.info("PAN photo not available.")

        st.subheader("PAN Details")
        p1, p2 = st.columns(2)
        with p1:
            pan_name = st.text_input("Name (as per PAN)", value=pan_name)
            pan_dob = st.text_input("Date of Birth (DD/MM/YYYY)", value=pan_dob)
        with p2:
            pan_father = st.text_input("Father's Name (as per PAN)", value=pan_father)
            pan_number = st.text_input("PAN Number", value=pan_number, max_chars=10)
        if not pan_number:
            st.warning("PAN number not detected from OCR. Please enter manually (format: AAAAA9999A).")

        st.subheader("Aadhaar Details")
        a1, a2 = st.columns(2)
        with a1:
            aadhaar_name = st.text_input("Name (as per Aadhaar)", value=aadhaar_name)
            aadhaar_dob = st.text_input("Date of Birth (YYYY-MM-DD)", value=aadhaar_dob)
        with a2:
            aadhaar_father = st.text_input("Care Of / Father / Spouse", value=aadhaar_father)
            aadhaar_number = st.text_input("Aadhaar Number", value=aadhaar_number, max_chars=12)
            aadhaar_address = st.text_area("Address", value=aadhaar_address, height=100)

        st.write("Validation & Deposit")
        vcol1, vcol2, vcol3 = st.columns([1, 1, 2])
        with vcol1:
            validate_pan_btn = st.form_submit_button("Validate PAN")
        with vcol2:
            validate_aadhaar_btn = st.form_submit_button("Validate Aadhaar")
        with vcol3:
            submit_btn = st.form_submit_button(submit_label)
        pay_col = st.container()
        with pay_col:
            deposit_amt = st.number_input("Deposit Amount (INR)", min_value=0, value=1000, step=500)
            pay_btn = st.form_submit_button("Pay Deposit (Razorpay sandbox)")

        if validate_pan_btn:
            if _validate_pan(pan_number):
                st.success("PAN format looks valid.")
            else:
                st.error("PAN format invalid. Expected pattern: AAAAA9999A.")

        if validate_aadhaar_btn:
            if _validate_aadhaar(aadhaar_number):
                st.success("Aadhaar number format looks valid.")
            else:
                st.error("Aadhaar should be a 12-digit number starting with 2-9.")

        if submit_btn:
            errors = []
            if pan_number and not _validate_pan(pan_number):
                errors.append("PAN format looks invalid.")
            if aadhaar_number and not _validate_aadhaar(aadhaar_number):
                errors.append("Aadhaar number format looks invalid.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.success("Details captured.")
                st.session_state["reviewed_form"] = {
                    "pan": {
                        "name": pan_name,
                        "father_name": pan_father,
                        "dob": pan_dob,
                        "pan_number": pan_number,
                    },
                    "aadhaar_number": aadhaar_number,
                    "aadhaar": {
                        "name": aadhaar_name,
                        "father_name": aadhaar_father,
                        "dob": aadhaar_dob,
                        "address": aadhaar_address,
                    },
                }
                st.session_state["step"] = advance_step
                st.rerun()

        if pay_btn:
            client = st.session_state.get("_api_client")
            if client is None:
                from services.api_client import KYCClient
                client = KYCClient()
                st.session_state["_api_client"] = client
            order = client.create_payment_order(deposit_amt * 100)
            st.session_state["deposit_order"] = order
            if order.get("order_id"):
                st.success(f"Created Razorpay test order: {order['order_id']} for INR {deposit_amt}")
            else:
                st.error(f"Failed to create order: {order}")
