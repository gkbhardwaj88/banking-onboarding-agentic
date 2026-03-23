# AI Banking Onboarding - Full Docker Setup

## Quick Start
1. Copy environment file:
   cp .env.sample .env

2. OCR runtimes:
   - Docker users: the backend image installs `tesseract-ocr` automatically.
   - Local dev: you can either install Tesseract (set `TESSERACT_CMD` in `.env` to the executable path) or rely on the built-in `easyocr` fallback (no system install required, but Python must have the `easyocr` package from `requirements.txt`).

3. Start system:
   docker-compose up --build

4. Access:
- Backend: http://localhost:8000
- Streamlit UI: http://localhost:8501
