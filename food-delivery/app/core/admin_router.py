from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.middleware.auth import require_role
from app.models.order import Order, OrderStatus
from app.models.restaurant import Restaurant
from app.models.user import RoleEnum, User

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/users")
def view_users(db: Session = Depends(get_db), _admin=Depends(require_role(RoleEnum.ADMIN))):
    return db.query(User).all()


@router.get("/orders")
def view_orders(db: Session = Depends(get_db), _admin=Depends(require_role(RoleEnum.ADMIN))):
    return db.query(Order).all()


@router.get("/restaurants")
def view_restaurants(db: Session = Depends(get_db), _admin=Depends(require_role(RoleEnum.ADMIN))):
    return db.query(Restaurant).all()


@router.put("/restaurants/{restaurant_id}/block")
def block_restaurant(restaurant_id: int, db: Session = Depends(get_db), _admin=Depends(require_role(RoleEnum.ADMIN))):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if restaurant:
        restaurant.is_blocked = True
        db.commit()
    return {"message": "Restaurant blocked"}


@router.put("/customers/{user_id}/block")
def block_customer(user_id: int, db: Session = Depends(get_db), _admin=Depends(require_role(RoleEnum.ADMIN))):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_blocked = True
        db.commit()
    return {"message": "Customer blocked"}


@router.get("/analytics")
def analytics(db: Session = Depends(get_db), _admin=Depends(require_role(RoleEnum.ADMIN))):
    total_orders = db.query(Order).count()
    cancelled_orders = db.query(Order).filter(Order.status == OrderStatus.CANCELLED).count()
    revenue = sum(o.total_amount for o in db.query(Order).filter(Order.status == OrderStatus.DELIVERED).all())
    return {
        "total_orders": total_orders,
        "cancelled_orders": cancelled_orders,
        "revenue": revenue,
    }
