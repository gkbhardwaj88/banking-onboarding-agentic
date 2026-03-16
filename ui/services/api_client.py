import requests

API_BASE = "http://localhost:8000"

class KYCClient:
    def send_kyc(self, aadhaar, pan):
        files = {}
        if aadhaar:
            files['aadhaar'] = (aadhaar.name, aadhaar.getvalue(), aadhaar.type or "image/png")
        if pan:
            files['pan'] = (pan.name, pan.getvalue(), pan.type or "image/png")
        resp = requests.post(f"{API_BASE}/kyc/process", files=files)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            # bubble up useful info even on non-200 responses
            return {"error": "backend_error", "status": resp.status_code, "body": resp.text}
        try:
            return resp.json()
        except ValueError:
            # response was not JSON; return raw text so UI doesn't crash
            return {"error": "invalid_json", "status": resp.status_code, "body": resp.text}

    def send_selfie(self, selfie_bytes):
        return {"status":"selfie received"}  # Placeholder

    def chat(self, msg):
        resp = requests.post(f"{API_BASE}/assistant/chat", params={"msg": msg})
        return resp.json()
