from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.api import auth, kyc, assistant, account, payment, agent

app = FastAPI(title="AI Banking Onboarding")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(kyc.router)
app.include_router(assistant.router)
app.include_router(account.router)
app.include_router(payment.router)
app.include_router(agent.router)

@app.get("/")
def root():
    return {"status": "backend running"}
