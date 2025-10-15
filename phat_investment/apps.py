from typing import final
from typing_extensions import override
from django.apps import AppConfig
from upstash_redis import Redis
import os
import logging


@final
class PhatInvestmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phat_investment"
    redis_client = None

    @override
    def ready(self) -> None:
        if self.redis_client is None:
            logging.info("Initilized phat_investment Redis")
            self.redis_client = Redis(
                url=os.environ.get("UPSTASH_REDIS_REST_URL") or "",
                token=os.environ.get("UPSTASH_REDIS_REST_TOKEN") or "",
            )
