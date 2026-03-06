from datetime import datetime

from pydantic import BaseModel

from app.models.withdraw_request import WithdrawStatus


class WithdrawCreate(BaseModel):
    amount: float
    upi_id: str


class WithdrawAction(BaseModel):
    status: WithdrawStatus


class WithdrawOut(BaseModel):
    id: int
    hosteller_id: int
    amount: float
    upi_id: str
    status: WithdrawStatus
    created_at: datetime

    class Config:
        from_attributes = True
