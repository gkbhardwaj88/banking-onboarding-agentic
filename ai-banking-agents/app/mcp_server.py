import json
from fastapi import FastAPI
from pydantic import BaseModel
from . import agent

# Minimal MCP-like HTTP wrapper exposing tools with JSON schemas
app = FastAPI(title="MCP Tool Server")

class ToolInvoke(BaseModel):
    tool: str
    params: dict

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "ocr_pan", "schema": {"type": "object", "properties": {"pan_bytes": {"type": "string", "description": "Base64 PAN image"}}}},
            {"name": "validate_aadhaar", "schema": {"type": "object", "properties": {"id_number": {"type": "string"}}}},
            {"name": "generate_otp", "schema": {"type": "object", "properties": {"id_number": {"type": "string"}}}},
            {"name": "submit_otp", "schema": {"type": "object", "properties": {"client_id": {"type": "string"}, "otp": {"type": "string"}}}},
            {"name": "create_payment_order", "schema": {"type": "object", "properties": {"amount_paise": {"type": "number"}}}},
        ]
    }

@app.post("/invoke")
def invoke(req: ToolInvoke):
    return agent.run_tool(req.tool, req.params)

@app.get("/")
def root():
    return {"status":"ok","message":"MCP tool server"}
