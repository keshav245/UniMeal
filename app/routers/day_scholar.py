from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import require_role
from app.models.order import Order, OrderStatus
from app.models.qr_code import QRCode
from app.models.transaction import Transaction
from app.models.user import User, UserRole
from app.schemas.order import CreateOrderRequest, OrderOut, VerifyPaymentRequest
from app.schemas.qr_code import QRCodeOut
from app.services.payment import payment_service
from app.services.wallet import settle_successful_order

router = APIRouter(prefix="/day-scholar", tags=["Day Scholar"])


@router.get("/qr-codes", response_model=list[QRCodeOut])
def browse_qr_codes(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.day_scholar)),
):
    _ = current_user
    return (
        db.query(QRCode)
        .filter(QRCode.is_active.is_(True))
        .order_by(QRCode.created_at.desc())
        .offset(offset)
        .limit(min(limit, 100))
        .all()
    )


@router.post("/orders", status_code=201)
def create_order(
    payload: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.day_scholar)),
):
    qr_code = db.query(QRCode).filter(QRCode.id == payload.qr_code_id, QRCode.is_active.is_(True)).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found")

    rp_order = payment_service.create_order(settings.qr_price_inr, receipt=f"order_{current_user.id}_{qr_code.id}")
    order = Order(
        buyer_id=current_user.id,
        qr_code_id=qr_code.id,
        amount=settings.qr_price_inr,
        status=OrderStatus.created,
        razorpay_order_id=rp_order["id"],
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"order": order, "gateway_order": rp_order, "amount": settings.qr_price_inr}


@router.post("/orders/verify", response_model=OrderOut)
def verify_payment(
    payload: VerifyPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.day_scholar)),
):
    order = (
        db.query(Order)
        .filter(Order.id == payload.order_id, Order.buyer_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == OrderStatus.paid:
        return order

    if order.razorpay_order_id != payload.razorpay_order_id:
        raise HTTPException(status_code=400, detail="Order mismatch")

    if not payment_service.verify_signature(
        payload.razorpay_order_id,
        payload.razorpay_payment_id,
        payload.razorpay_signature,
    ):
        order.status = OrderStatus.failed
        db.commit()
        raise HTTPException(status_code=400, detail="Payment signature verification failed")

    order.status = OrderStatus.paid
    order.razorpay_payment_id = payload.razorpay_payment_id
    qr_code = db.query(QRCode).filter(QRCode.id == order.qr_code_id).first()
    settle_successful_order(db, order.id, qr_code)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders", response_model=list[OrderOut])
def purchased_qr_codes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.day_scholar)),
):
    return (
        db.query(Order)
        .filter(Order.buyer_id == current_user.id, Order.status == OrderStatus.paid)
        .order_by(Order.created_at.desc())
        .all()
    )


@router.get("/transactions")
def transaction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.day_scholar)),
):
    rows = (
        db.query(Transaction)
        .join(Order, Transaction.order_id == Order.id)
        .filter(Order.buyer_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .all()
    )
    return rows
