from fastapi import APIRouter

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/create")
def create(acc_type: str):
    return {"status": "created", "account_type": acc_type}
