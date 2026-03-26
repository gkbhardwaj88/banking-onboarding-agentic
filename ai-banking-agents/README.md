# AI Banking Agents (Agentic Chatbot Edition)

Minimal FastAPI-based agentic chatbot for banking onboarding:
- Agent orchestrator (LangGraph) that suggests and calls tools (PAN OCR, Aadhaar validate/OTP via Surepass, payment order stub).
- MCP-ready: agent tools exposed via HTTP; can be wrapped as MCP tools.
- Razorpay sandbox is stubbed; Surepass sandbox used for Aadhaar.

Run
```
python -m venv venv
venv/Scripts/activate  # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set DB URL, JWT, Surepass token
uvicorn app.main:app --reload
```

