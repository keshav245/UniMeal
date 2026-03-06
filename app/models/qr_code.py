from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class QRCode(Base):
    __tablename__ = "qr_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hosteller_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    sales_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hosteller = relationship("User", back_populates="uploaded_qr_codes")
    orders = relationship("Order", back_populates="qr_code")
