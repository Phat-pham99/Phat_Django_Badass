from django.apps import AppConfig
from upstash_redis import Redis
import os
import logging

class PhatInvestmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phat_investment"
    redis_client = None

    def ready(self):
        if PhatInvestmentConfig.redis_client is None:
            logging.info("Initilized phat_investment Redis")
            PhatInvestmentConfig.redis_client = Redis(
                url=os.environ.get("UPSTASH_REDIS_REST_URL"),
                token=os.environ.get("UPSTASH_REDIS_REST_TOKEN")
                )