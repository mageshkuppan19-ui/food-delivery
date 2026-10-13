from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.session import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="foods")
    images = relationship("FoodImage", back_populates="food")


class FoodImage(Base):
    __tablename__ = "food_images"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    url = Column(String(500), nullable=False)

    food = relationship("Food", back_populates="images")
