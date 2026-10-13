from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.middleware.auth import get_current_user
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
def get_notifications(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Notification).filter(Notification.user_id == user.id).all()


@router.put("/{notification_id}/read")
def mark_as_read(notification_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user.id)
        .first()
    )
    if notification:
        notification.is_read = True
        db.commit()
    return {"message": "ok"}
