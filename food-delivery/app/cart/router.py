from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.cart import add_item, get_or_create_cart, remove_item
from app.database.session import get_db
from app.middleware.auth import require_role
from app.models.user import RoleEnum
from app.schemas.cart import CartItemCreate, CartOut

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("", response_model=CartOut)
def add_to_cart(
    payload: CartItemCreate,
    db: Session = Depends(get_db),
    customer=Depends(require_role(RoleEnum.CUSTOMER)),
):
    return add_item(db, customer.id, payload.food_id, payload.quantity)


@router.get("", response_model=CartOut)
def view_cart(db: Session = Depends(get_db), customer=Depends(require_role(RoleEnum.CUSTOMER))):
    return get_or_create_cart(db, customer.id)


@router.delete("/{item_id}", response_model=CartOut)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    customer=Depends(require_role(RoleEnum.CUSTOMER)),
):
    return remove_item(db, customer.id, item_id)
