from fastapi import APIRouter

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/deposit")
def deposit(amount: int, method: str):
    return {"status": "success", "amount": amount, "method": method}
