import json

from kafka import KafkaConsumer

from app.core.config import settings
from app.database.session import SessionLocal
from app.models.notification import NotificationChannel
from app.services.notification_service import send_notification

NOTIFICATION_TOPIC = "order-events"


def run_consumer() -> None:
    """Run as a standalone worker process: `python -m app.kafka.consumer`."""
    consumer = KafkaConsumer(
        NOTIFICATION_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="notification-workers",
    )
    for message in consumer:
        event = message.value
        db = SessionLocal()
        try:
            send_notification(
                db,
                user_id=event["user_id"],
                channel=NotificationChannel(event.get("channel", "push")),
                title=event.get("title", "Order update"),
                body=event.get("body", ""),
            )
        finally:
            db.close()


if __name__ == "__main__":
    run_consumer()
