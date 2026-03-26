from fastapi import APIRouter
from ..services import payment
router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/order")
def create_order(amount_paise: int, currency: str="INR"):
    return payment.create_order(amount_paise, currency)
