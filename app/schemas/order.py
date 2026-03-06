from datetime import datetime

from pydantic import BaseModel

from app.models.order import OrderStatus


class CreateOrderRequest(BaseModel):
    qr_code_id: int


class VerifyPaymentRequest(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class OrderOut(BaseModel):
    id: int
    buyer_id: int
    qr_code_id: int
    amount: float
    status: OrderStatus
    razorpay_order_id: str | None
    razorpay_payment_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True
