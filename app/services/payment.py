import hashlib
import hmac
import uuid

import razorpay

from app.core.config import settings


class PaymentService:
    def __init__(self):
        self.client = None
        if settings.razorpay_key_id and settings.razorpay_key_secret:
            self.client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))

    def create_order(self, amount_inr: int, receipt: str) -> dict:
        amount_paise = amount_inr * 100
        if self.client:
            return self.client.order.create(
                {
                    "amount": amount_paise,
                    "currency": settings.payment_currency,
                    "receipt": receipt,
                    "payment_capture": 1,
                }
            )
        return {"id": f"order_{uuid.uuid4().hex[:12]}", "amount": amount_paise, "currency": "INR"}

    def verify_signature(self, razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
        if not settings.razorpay_key_secret:
            return razorpay_signature == "dev_signature"

        payload = f"{razorpay_order_id}|{razorpay_payment_id}"
        expected = hmac.new(
            settings.razorpay_key_secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, razorpay_signature)


payment_service = PaymentService()
