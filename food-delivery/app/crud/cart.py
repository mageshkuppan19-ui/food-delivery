from sqlalchemy.orm import Session

from app.models.cart import Cart, CartItem


def get_or_create_cart(db: Session, customer_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def add_item(db: Session, customer_id: int, food_id: int, quantity: int) -> Cart:
    cart = get_or_create_cart(db, customer_id)
    item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.food_id == food_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, food_id=food_id, quantity=quantity)
        db.add(item)
    db.commit()
    db.refresh(cart)
    return cart


def remove_item(db: Session, customer_id: int, item_id: int) -> Cart:
    cart = get_or_create_cart(db, customer_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if item:
        db.delete(item)
        db.commit()
    db.refresh(cart)
    return cart
