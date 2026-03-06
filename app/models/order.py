import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OrderStatus(str, enum.Enum):
    created = "created"
    paid = "paid"
    failed = "failed"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    qr_code_id: Mapped[int] = mapped_column(ForeignKey("qr_codes.id", ondelete="CASCADE"), index=True)

    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.created, index=True)
    razorpay_order_id: Mapped[str] = mapped_column(String(120), nullable=True)
    razorpay_payment_id: Mapped[str] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    buyer = relationship("User", back_populates="orders")
    qr_code = relationship("QRCode", back_populates="orders")
    transaction = relationship("Transaction", back_populates="order", uselist=False)
