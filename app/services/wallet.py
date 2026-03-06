from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.qr_code import QRCode
from app.models.transaction import Transaction
from app.models.user import User


def settle_successful_order(db: Session, order_id: int, qr_code: QRCode) -> Transaction:
    hosteller = db.query(User).filter(User.id == qr_code.hosteller_id).first()
    tx = Transaction(
        order_id=order_id,
        hosteller_id=hosteller.id,
        gross_amount=settings.qr_price_inr,
        hosteller_share=settings.hosteller_share_inr,
        admin_share=settings.admin_share_inr,
    )
    hosteller.wallet_balance = float(hosteller.wallet_balance) + settings.hosteller_share_inr
    hosteller.total_earnings = float(hosteller.total_earnings) + settings.hosteller_share_inr
    qr_code.sales_count += 1
    db.add(tx)
    return tx
