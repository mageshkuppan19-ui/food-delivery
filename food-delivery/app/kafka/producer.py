import json

from kafka import KafkaProducer

from app.core.config import settings

_producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return _producer


def publish_event(topic: str, payload: dict) -> None:
    producer = get_producer()
    producer.send(topic, payload)
    producer.flush()
