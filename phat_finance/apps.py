# .phat_finance/apps.py
from django.apps import AppConfig
from upstash_redis import Redis
import os
import logging


class PhatFinanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phat_finance"
    redis_client = None

    def ready(self) -> None:
        if PhatFinanceConfig.redis_client is None:
            logging.info("Initilized phat_finance Redis")
            PhatFinanceConfig.redis_client = Redis(
                url=os.environ.get("UPSTASH_REDIS_REST_URL"),
                token=os.environ.get("UPSTASH_REDIS_REST_TOKEN"),
            )
