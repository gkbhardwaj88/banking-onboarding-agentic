import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/payment", tags=["Payment"])


class OrderRequest(BaseModel):
    amount: int  # in paise
    currency: str = "INR"
    notes: dict | None = None


class VerifyRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str


@router.post("/order")
def create_order(req: OrderRequest):
    """
    Placeholder Razorpay order creator (sandbox). In production, call Razorpay Orders API here.
    """
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    order_id = f"order_{uuid.uuid4().hex[:14]}"
    return {
        "order_id": order_id,
        "amount": req.amount,
        "currency": req.currency,
        "status": "created",
        "provider": "razorpay-sandbox-placeholder",
        "notes": req.notes or {},
    }


@router.post("/verify")
def verify_payment(req: VerifyRequest):
    """
    Placeholder verification. In production, verify Razorpay signature server-side.
    """
    # For now, accept any signature
    return {
        "order_id": req.order_id,
        "payment_id": req.payment_id,
        "status": "captured",
        "provider": "razorpay-sandbox-placeholder",
    }
