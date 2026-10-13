from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.food import create_food, delete_food, get_food, list_foods, update_food
from app.database.session import get_db
from app.middleware.auth import require_role
from app.models.user import RoleEnum
from app.schemas.food import FoodCreate, FoodOut, FoodUpdate

router = APIRouter(prefix="/foods", tags=["Menu"])


@router.post("", response_model=FoodOut, status_code=201)
def add_food(
    payload: FoodCreate,
    db: Session = Depends(get_db),
    _owner=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.ADMIN)),
):
    return create_food(db, payload)


@router.get("", response_model=list[FoodOut])
def get_foods(restaurant_id: int | None = None, db: Session = Depends(get_db)):
    return list_foods(db, restaurant_id)


@router.get("/{food_id}", response_model=FoodOut)
def get_food_by_id(food_id: int, db: Session = Depends(get_db)):
    food = get_food(db, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.put("/{food_id}", response_model=FoodOut)
def edit_food(
    food_id: int,
    payload: FoodUpdate,
    db: Session = Depends(get_db),
    _owner=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.ADMIN)),
):
    food = update_food(db, food_id, payload)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.delete("/{food_id}", status_code=204)
def remove_food(
    food_id: int,
    db: Session = Depends(get_db),
    _owner=Depends(require_role(RoleEnum.RESTAURANT, RoleEnum.ADMIN)),
):
    delete_food(db, food_id)
    return None
