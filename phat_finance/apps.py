# .phat_finance/apps.py
import logging
import os
from typing import final

from django.apps import AppConfig
from typing_extensions import override
from upstash_redis import Redis


@final
class PhatFinanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name: str = "phat_finance"
    redis_client: Redis = None

    @override
    def ready(self) -> None:
        if self.redis_client is None:
            logging.info("Initilized phat_finance Redis")
            self.redis_client = Redis(
                url=os.environ.get("UPSTASH_REDIS_REST_URL") or "",
                token=os.environ.get("UPSTASH_REDIS_REST_TOKEN") or "",
            )
