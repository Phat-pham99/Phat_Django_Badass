from typing import final

from django.apps import AppConfig


@final
class RedisUiConfig(AppConfig):
    name = "redis_ui"