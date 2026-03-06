from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.order import Order
from app.models.qr_code import QRCode
from app.models.user import User, UserRole
from app.models.withdraw_request import WithdrawRequest
from app.schemas.qr_code import QRCodeOut
from app.schemas.withdraw import WithdrawCreate, WithdrawOut
from app.services.storage import upload_qr_image

router = APIRouter(prefix="/hosteller", tags=["Hosteller"])


@router.post("/qr-codes", response_model=QRCodeOut, status_code=201)
def upload_qr_code(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.hosteller)),
):
    image_url = upload_qr_image(file)
    qr_code = QRCode(hosteller_id=current_user.id, title=title, image_url=image_url)
    db.add(qr_code)
    db.commit()
    db.refresh(qr_code)
    return qr_code


@router.get("/qr-codes", response_model=list[QRCodeOut])
def list_uploaded_qr_codes(
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.hosteller))
):
    return db.query(QRCode).filter(QRCode.hosteller_id == current_user.id).all()


@router.get("/sales")
def qr_sales_summary(
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.hosteller))
):
    total_sales = (
        db.query(Order)
        .join(QRCode, Order.qr_code_id == QRCode.id)
        .filter(QRCode.hosteller_id == current_user.id, Order.status == "paid")
        .count()
    )
    return {
        "wallet_balance": float(current_user.wallet_balance),
        "total_earnings": float(current_user.total_earnings),
        "total_sales": total_sales,
    }


@router.post("/withdraw", response_model=WithdrawOut, status_code=201)
def request_withdraw(
    payload: WithdrawCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.hosteller)),
):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if float(current_user.wallet_balance) < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance")

    wr = WithdrawRequest(hosteller_id=current_user.id, amount=payload.amount, upi_id=payload.upi_id)
    current_user.wallet_balance = float(current_user.wallet_balance) - payload.amount
    db.add(wr)
    db.commit()
    db.refresh(wr)
    return wr
