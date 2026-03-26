import uuid


def create_order_placeholder(amount_paise: int, currency: str = "INR"):
    """
    Placeholder for Razorpay order creation. Returns a fake order id.
    """
    return {
        "order_id": f"order_{uuid.uuid4().hex[:14]}",
        "amount": amount_paise,
        "currency": currency,
        "status": "created",
        "provider": "razorpay-sandbox-placeholder",
    }
