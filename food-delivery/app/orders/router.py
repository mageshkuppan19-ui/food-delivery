from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.order import create_order_from_cart, get_order, list_orders, update_order_status
from app.database.session import get_db
from app.middleware.auth import get_current_user, require_role
from app.models.user import RoleEnum
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderOut, status_code=201)
def place_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    customer=Depends(require_role(RoleEnum.CUSTOMER)),
):
    try:
        return create_order_from_cart(db, customer.id, payload.restaurant_id, payload.address_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    customer_id = user.id if user.role == RoleEnum.CUSTOMER else None
    return list_orders(db, customer_id)


@router.get("/{order_id}", response_model=OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}/status", response_model=OrderOut)
def change_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.DELIVERY_PARTNER, RoleEnum.ADMIN)),
):
    order = update_order_status(db, order_id, payload.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
