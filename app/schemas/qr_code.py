from datetime import datetime

from pydantic import BaseModel


class QRCodeCreate(BaseModel):
    title: str


class QRCodeOut(BaseModel):
    id: int
    hosteller_id: int
    title: str
    image_url: str
    sales_count: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
