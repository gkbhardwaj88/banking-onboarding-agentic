# AI Banking Onboarding - Full Docker Setup

## Quick Start
1. Copy environment file:
   cp .env.sample .env

2. Make sure OCR runtime is available:
   - Docker users: the backend image installs `tesseract-ocr` automatically.
   - Local dev on Windows/macOS: install Tesseract and set `TESSERACT_CMD` in `.env` to the full path (e.g. `C:\\Program Files\\Tesseract-OCR\\tesseract.exe` on Windows).

3. Start system:
   docker-compose up --build

4. Access:
- Backend: http://localhost:8000
- Streamlit UI: http://localhost:8501
