from pydantic import BaseModel


class ReviewCreate(BaseModel):
    restaurant_id: int | None = None
    food_id: int | None = None
    restaurant_rating: int | None = None
    food_rating: int | None = None
    comment: str | None = None


class ReviewOut(ReviewCreate):
    id: int
    customer_id: int

    class Config:
        from_attributes = True
