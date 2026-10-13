from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.database.session import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    address = Column(String(255), nullable=False)
    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)
    is_open = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("RestaurantImage", back_populates="restaurant")
    foods = relationship("Food", back_populates="restaurant")


class RestaurantImage(Base):
    __tablename__ = "restaurant_images"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    url = Column(String(500), nullable=False)

    restaurant = relationship("Restaurant", back_populates="images")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
