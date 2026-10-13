"""Background notification dispatch: email, SMS, push.

Called from Kafka consumers or directly from route handlers via
FastAPI's BackgroundTasks.
"""

from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationChannel


def send_notification(
    db: Session,
    user_id: int,
    channel: NotificationChannel,
    title: str,
    body: str,
) -> Notification:
    # Plug in a real provider here (SES/SendGrid for email, Twilio for SMS, FCM for push).
    notification = Notification(user_id=user_id, channel=channel, title=title, body=body)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
