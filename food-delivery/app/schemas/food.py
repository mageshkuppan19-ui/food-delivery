from pydantic import BaseModel


class FoodBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    available: bool = True
    category_id: int | None = None


class FoodCreate(FoodBase):
    restaurant_id: int


class FoodUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    available: bool | None = None
    category_id: int | None = None


class FoodOut(FoodBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True
