from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.middleware.auth import require_role
from app.models.review import Review
from app.models.user import RoleEnum
from app.schemas.review import ReviewCreate, ReviewOut

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewOut, status_code=201)
def add_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    customer=Depends(require_role(RoleEnum.CUSTOMER)),
):
    review = Review(customer_id=customer.id, **payload.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("", response_model=list[ReviewOut])
def get_reviews(
    restaurant_id: int | None = None,
    food_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Review)
    if restaurant_id:
        query = query.filter(Review.restaurant_id == restaurant_id)
    if food_id:
        query = query.filter(Review.food_id == food_id)
    return query.all()
