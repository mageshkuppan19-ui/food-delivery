import redis

from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def cache_set(key: str, value: str, expire_seconds: int = 300) -> None:
    redis_client.set(key, value, ex=expire_seconds)


def cache_get(key: str) -> str | None:
    return redis_client.get(key)
