from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.middleware.auth import require_role
from app.models.delivery import Delivery
from app.models.user import RoleEnum
from app.schemas.delivery import DeliveryAssign, DeliveryLocationUpdate, DeliveryOut

router = APIRouter(prefix="/deliveries", tags=["Delivery"])


@router.post("/assign", response_model=DeliveryOut, status_code=201)
def assign_delivery_partner(
    payload: DeliveryAssign,
    db: Session = Depends(get_db),
    _staff=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.ADMIN)),
):
    delivery = Delivery(order_id=payload.order_id, delivery_partner_id=payload.delivery_partner_id)
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery


@router.get("/{order_id}", response_model=DeliveryOut)
def track_delivery(order_id: int, db: Session = Depends(get_db), _user=Depends(require_role(
    RoleEnum.CUSTOMER, RoleEnum.RESTAURANT, RoleEnum.DELIVERY_PARTNER, RoleEnum.ADMIN
))):
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.put("/{order_id}/location", response_model=DeliveryOut)
def update_location(
    order_id: int,
    payload: DeliveryLocationUpdate,
    db: Session = Depends(get_db),
    _partner=Depends(require_role(RoleEnum.DELIVERY_PARTNER)),
):
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    delivery.current_location = payload.current_location
    db.commit()
    db.refresh(delivery)
    return delivery
