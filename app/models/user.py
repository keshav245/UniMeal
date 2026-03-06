import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    hosteller = "hosteller"
    day_scholar = "day_scholar"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    wallet_balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    total_earnings: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    uploaded_qr_codes = relationship("QRCode", back_populates="hosteller")
    orders = relationship("Order", back_populates="buyer")
    withdrawals = relationship("WithdrawRequest", back_populates="hosteller")
