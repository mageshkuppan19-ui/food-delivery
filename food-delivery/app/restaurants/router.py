from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.restaurant import create_restaurant, get_restaurant, list_restaurants, update_restaurant
from app.database.session import get_db
from app.middleware.auth import require_role
from app.models.user import RoleEnum
from app.schemas.restaurant import RestaurantCreate, RestaurantOut, RestaurantUpdate

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.post("", response_model=RestaurantOut, status_code=201)
def add_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db),
    owner=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.ADMIN)),
):
    return create_restaurant(db, owner.id, payload)


@router.get("", response_model=list[RestaurantOut])
def get_restaurants(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return list_restaurants(db, skip, limit)


@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantOut)
def edit_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    db: Session = Depends(get_db),
    _owner=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.ADMIN)),
):
    restaurant = update_restaurant(db, restaurant_id, payload)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
