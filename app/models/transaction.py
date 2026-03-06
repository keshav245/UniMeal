from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), unique=True, index=True)
    hosteller_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    gross_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    hosteller_share: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    admin_share: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_gateway: Mapped[str] = mapped_column(String(30), default="razorpay")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="transaction")
