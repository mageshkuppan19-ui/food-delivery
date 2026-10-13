from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.food import Food
from app.models.order import Order, OrderItem, OrderStatus


def create_order_from_cart(db: Session, customer_id: int, restaurant_id: int, address_id: int) -> Order:
    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()
    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    order = Order(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        address_id=address_id,
        status=OrderStatus.PENDING,
        total_amount=0.0,
    )
    db.add(order)
    db.flush()

    total = 0.0
    for cart_item in cart.items:
        food = db.query(Food).filter(Food.id == cart_item.food_id).first()
        if not food:
            continue
        line_total = food.price * cart_item.quantity
        total += line_total
        db.add(
            OrderItem(
                order_id=order.id,
                food_id=food.id,
                food_name=food.name,
                quantity=cart_item.quantity,
                price=food.price,
            )
        )

    order.total_amount = total
    for cart_item in list(cart.items):
        db.delete(cart_item)

    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def list_orders(db: Session, customer_id: int | None = None, skip: int = 0, limit: int = 50) -> list[Order]:
    query = db.query(Order)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    return query.offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, status: OrderStatus) -> Order | None:
    order = get_order(db, order_id)
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order
