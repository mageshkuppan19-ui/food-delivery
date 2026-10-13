from pydantic import BaseModel

from app.models.payment import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    method: PaymentMethod


class PaymentOut(BaseModel):
    id: int
    order_id: int
    method: PaymentMethod
    status: PaymentStatus
    amount: float

    class Config:
        from_attributes = True
