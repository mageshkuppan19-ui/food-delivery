from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.cart.router import router as cart_router
from app.core.admin_router import router as admin_router
from app.core.config import settings
from app.database.session import Base, engine
from app.delivery.router import router as delivery_router
from app.menu.router import router as menu_router
from app.notifications.router import router as notifications_router
from app.orders.router import router as orders_router
from app.payment.router import router as payment_router
from app.restaurants.router import router as restaurants_router
from app.reviews.router import router as reviews_router
from app.users.router import router as users_router

# Import models so SQLAlchemy registers them on Base.metadata
from app.models import cart, delivery, food, notification, order, payment, restaurant, review, user  # noqa: F401

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def on_startup() -> None:
    # For quick local dev only — use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(restaurants_router)
app.include_router(menu_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(payment_router)
app.include_router(delivery_router)
app.include_router(reviews_router)
app.include_router(notifications_router)
app.include_router(admin_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
