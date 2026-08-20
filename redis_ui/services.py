from typing import Any

from django.apps import apps


def get_redis():
    """Lazily return the shared Upstash REST client.

    Reuses phat_finance's client to avoid a third connection.
    """
    config = apps.get_app_config("phat_finance")
    client = config.redis_client
    if client is None:
        config.ready()
        client = config.redis_client
    return client


def list_keys(pattern: str = "*", count: int = 100):
    """Non-blocking SCAN. Returns (keys, next_cursor)."""
    redis = get_redis()
    cursor, keys = redis.scan(0, match=pattern, count=count)
    all_keys = list(keys)
    while cursor != 0 and len(all_keys) < count:
        cursor, keys = redis.scan(cursor, match=pattern, count=count)
        all_keys.extend(keys)
    return all_keys[:count], cursor


def get_key_info(key: str) -> dict[str, Any]:
    """Safe query: value, type, ttl, exists."""
    redis = get_redis()
    return {
        "key": key,
        "exists": redis.exists(key),
        "type": redis.type(key),
        "ttl": redis.ttl(key),
        "value": redis.get(key),
    }


def set_key(key: str, value: str, ttl_seconds: int | None = None) -> Any:
    """Safe set with optional expiration."""
    redis = get_redis()
    kwargs: dict[str, int] = {}
    if ttl_seconds is not None and ttl_seconds > 0:
        kwargs["ex"] = ttl_seconds
    return redis.set(key, value, **kwargs)


def delete_key(key: str) -> Any:
    """Safe delete. Returns number of keys removed."""
    redis = get_redis()
    return redis.delete(key)