import requests, json

AZURE_ENDPOINT = "https://your-azure.cognitiveservices.azure.com/"
AZURE_KEY = "CHANGE_ME"

def azure_ocr(image_bytes: bytes):
    url = AZURE_ENDPOINT + "formrecognizer/documentModels/prebuilt-id:analyze?api-version=2023-07-31"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }
    resp = requests.post(url, headers=headers, data=image_bytes)
    resp.raise_for_status()
    return resp.json()
