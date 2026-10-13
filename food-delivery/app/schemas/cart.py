from pydantic import BaseModel


class CartItemCreate(BaseModel):
    food_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    id: int
    food_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: int
    customer_id: int
    items: list[CartItemOut] = []

    class Config:
        from_attributes = True
