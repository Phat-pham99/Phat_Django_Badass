from django.apps import apps
from django.db import models
from datetime import date, datetime
from django.db import transaction
import logging

from django.db.models.options import override
from ..enums.investment_enums import INVESTMENT_ENUM

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_investment").redis_client
if redis is None:
    apps.get_app_config("phat_investment").ready()  # Important, bruh
    redis = apps.get_app_config("phat_investment").redis_client
else:
    print("Redis client initialized in phat_investment app config")

class Investment(models.Model):
    date = models.DateField(default=date.today)
    investment_type = models.CharField(max_length=15, choices=INVESTMENT_ENUM)
    amount = models.PositiveIntegerField(blank=True, default=0)

    @transaction.atomic
    def __invest(
        self,
        investment_type: str,
        amount: int) -> None:
        """
        Invest into assets 🪙💹. Deduct balance.digital accordingly
        @param investment_type(str) My current investment \
        (stock, Vincapital, DragonCapital, crypto currency)
        @param amount(int) Money, VND
        """
        pipeline = redis.multi()
        pipeline.decrby("balance_digital", amount)
        pipeline.incrby("total_investment", amount)
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Invest to {investment_type}",
            }
        )
        pipeline.exec()

    @override
    def __save(self, *args, **kwargs):
        self.__invest(self.investment_type, self.amount)
        super().__save(*args, **kwargs)
