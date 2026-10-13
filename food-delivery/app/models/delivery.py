from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.database.session import Base


class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    vehicle_number = Column(String(20), nullable=True)
    is_available = Column(Boolean, default=True)
    current_latitude = Column(String(50), nullable=True)
    current_longitude = Column(String(50), nullable=True)


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    delivery_partner_id = Column(Integer, ForeignKey("delivery_partners.id"), nullable=True)
    current_location = Column(String(255), nullable=True)
    estimated_time_minutes = Column(Integer, nullable=True)
    picked_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
