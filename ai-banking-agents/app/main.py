from fastapi import FastAPI
from .db import Base, engine
from .routers import kyc, payment, agent as agent_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Banking Agentic Chatbot")
app.include_router(kyc.router)
app.include_router(payment.router)
app.include_router(agent_router.router)

@app.get("/")
def root():
    return {"status": "ok"}
