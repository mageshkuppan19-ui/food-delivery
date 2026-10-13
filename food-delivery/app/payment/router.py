from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.middleware.auth import get_current_user
from app.models.order import Order
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payment"])


@router.post("", response_model=PaymentOut, status_code=201)
def make_payment(payload: PaymentCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Mock payment gateway: cash is pending until delivery, upi/card mark paid immediately.
    status_ = PaymentStatus.PENDING if payload.method.value == "cash" else PaymentStatus.PAID

    payment = Payment(order_id=order.id, method=payload.method, status=status_, amount=order.total_amount)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.get("/{order_id}", response_model=PaymentOut)
def get_payment(order_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.order_id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
