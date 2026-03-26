import uuid

def create_order(amount_paise:int, currency:str="INR"):
    return {
        "order_id": f"order_{uuid.uuid4().hex[:14]}",
        "amount": amount_paise,
        "currency": currency,
        "status": "created",
    }
