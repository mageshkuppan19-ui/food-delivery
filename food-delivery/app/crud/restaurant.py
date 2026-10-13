from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def create_restaurant(db: Session, owner_id: int, payload: RestaurantCreate) -> Restaurant:
    restaurant = Restaurant(owner_id=owner_id, **payload.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurant(db: Session, restaurant_id: int) -> Restaurant | None:
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def list_restaurants(db: Session, skip: int = 0, limit: int = 50) -> list[Restaurant]:
    return db.query(Restaurant).offset(skip).limit(limit).all()


def update_restaurant(db: Session, restaurant_id: int, payload: RestaurantUpdate) -> Restaurant | None:
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(restaurant, field, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant
