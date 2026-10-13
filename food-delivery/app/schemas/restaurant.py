from datetime import time

from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    description: str | None = None
    address: str
    opening_time: time | None = None
    closing_time: time | None = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
    opening_time: time | None = None
    closing_time: time | None = None
    is_open: bool | None = None


class RestaurantOut(RestaurantBase):
    id: int
    owner_id: int
    is_open: bool
    rating: float

    class Config:
        from_attributes = True
