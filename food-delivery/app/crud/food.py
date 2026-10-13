from sqlalchemy.orm import Session

from app.models.food import Food
from app.schemas.food import FoodCreate, FoodUpdate


def create_food(db: Session, payload: FoodCreate) -> Food:
    food = Food(**payload.model_dump())
    db.add(food)
    db.commit()
    db.refresh(food)
    return food


def get_food(db: Session, food_id: int) -> Food | None:
    return db.query(Food).filter(Food.id == food_id).first()


def list_foods(db: Session, restaurant_id: int | None = None, skip: int = 0, limit: int = 50) -> list[Food]:
    query = db.query(Food)
    if restaurant_id:
        query = query.filter(Food.restaurant_id == restaurant_id)
    return query.offset(skip).limit(limit).all()


def update_food(db: Session, food_id: int, payload: FoodUpdate) -> Food | None:
    food = get_food(db, food_id)
    if not food:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(food, field, value)
    db.commit()
    db.refresh(food)
    return food


def delete_food(db: Session, food_id: int) -> None:
    food = get_food(db, food_id)
    if food:
        db.delete(food)
        db.commit()
