from django.apps import apps
from django.db import models
from typing import final
from datetime import datetime
from django.db import transaction
from types import NoneType
from logging import Logger, getLogger
from upstash_redis import Redis
from ..enums.finance_enums import CREDITCARD_ENUM

logger: Logger = getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    logger.info("Redis client initialized in phat_finance app config")

@final
class CreditCardPayment(models.Model):
    term = models.CharField(max_length=7, blank=False, null=False)
    amount = models.PositiveIntegerField(blank=True, default=0, null=False)
    card = models.CharField(
        max_length=20, choices=CREDITCARD_ENUM, null=False, default="VISA Platinum"
    )
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f"Credit card payment - {self.term}: {self.amount} VND💸"

    @transaction.atomic
    def __pay_creditCard(
        self,
        redis_client: Redis,
        amount: int) -> None:
        """
        Decrease digital 🏧 balance by {amount} on Redis
        """
        pipeline = redis_client.multi()
        pipeline.decrby("balance_digital", amount)
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Pay credit card 💳 bill: {amount}",
            }
        )
        pipeline.exec()

    def save(self, *args, **kwargs) -> None:
        if type(self.amount) == NoneType:
            self.amount = 0
        self.__pay_creditCard(redis, self.amount)
        super().save(*args, **kwargs)  # Over-write the save() method
