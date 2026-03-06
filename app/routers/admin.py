from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.order import Order, OrderStatus
from app.models.qr_code import QRCode
from app.models.transaction import Transaction
from app.models.user import User, UserRole
from app.models.withdraw_request import WithdrawRequest, WithdrawStatus
from app.schemas.user import UserOut
from app.schemas.withdraw import WithdrawAction, WithdrawOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))
):
    _ = current_user
    total_users = db.query(func.count(User.id)).scalar()
    total_qr_uploads = db.query(func.count(QRCode.id)).scalar()
    total_qr_sales = db.query(func.count(Order.id)).filter(Order.status == OrderStatus.paid).scalar()
    gross_revenue = db.query(func.coalesce(func.sum(Transaction.gross_amount), 0)).scalar()
    admin_revenue = db.query(func.coalesce(func.sum(Transaction.admin_share), 0)).scalar()

    return {
        "total_users": total_users,
        "total_qr_uploads": total_qr_uploads,
        "total_qr_sales": total_qr_sales,
        "gross_revenue": float(gross_revenue or 0),
        "admin_revenue": float(admin_revenue or 0),
    }


@router.get("/users", response_model=list[UserOut])
def list_users(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    _ = current_user
    return db.query(User).offset(offset).limit(min(limit, 200)).all()


@router.patch("/users/{user_id}/toggle")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    _ = current_user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"id": user.id, "is_active": user.is_active}


@router.get("/qr-codes")
def manage_qr_codes(
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))
):
    _ = current_user
    return db.query(QRCode).order_by(QRCode.created_at.desc()).all()


@router.patch("/qr-codes/{qr_id}/toggle")
def toggle_qr(
    qr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    _ = current_user
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR not found")
    qr.is_active = not qr.is_active
    db.commit()
    return {"id": qr.id, "is_active": qr.is_active}


@router.get("/transactions")
def monitor_transactions(
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))
):
    _ = current_user
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()


@router.get("/withdraw-requests", response_model=list[WithdrawOut])
def list_withdraw_requests(
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))
):
    _ = current_user
    return db.query(WithdrawRequest).order_by(WithdrawRequest.created_at.desc()).all()


@router.patch("/withdraw-requests/{request_id}", response_model=WithdrawOut)
def update_withdraw_request(
    request_id: int,
    payload: WithdrawAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    _ = current_user
    wr = db.query(WithdrawRequest).filter(WithdrawRequest.id == request_id).first()
    if not wr:
        raise HTTPException(status_code=404, detail="Withdraw request not found")

    if wr.status != WithdrawStatus.pending:
        raise HTTPException(status_code=400, detail="Request is already processed")

    if payload.status == WithdrawStatus.rejected:
        hosteller = db.query(User).filter(User.id == wr.hosteller_id).first()
        hosteller.wallet_balance = float(hosteller.wallet_balance) + float(wr.amount)

    wr.status = payload.status
    db.commit()
    db.refresh(wr)
    return wr
