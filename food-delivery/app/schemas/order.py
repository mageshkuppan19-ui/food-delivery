from datetime import datetime

from pydantic import BaseModel

from app.models.order import OrderStatus


class OrderItemOut(BaseModel):
    id: int
    food_id: int
    food_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    restaurant_id: int
    address_id: int


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderOut(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    delivery_partner_id: int | None
    status: OrderStatus
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut] = []

    class Config:
        from_attributes = True
