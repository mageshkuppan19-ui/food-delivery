from pydantic import BaseModel


class DeliveryAssign(BaseModel):
    order_id: int
    delivery_partner_id: int


class DeliveryLocationUpdate(BaseModel):
    current_location: str


class DeliveryOut(BaseModel):
    id: int
    order_id: int
    delivery_partner_id: int | None
    current_location: str | None
    estimated_time_minutes: int | None

    class Config:
        from_attributes = True
