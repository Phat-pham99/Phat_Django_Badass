from django.apps import apps
from django.db import models
from datetime import date, datetime
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_investment").redis_client
if redis is None:
    apps.get_app_config("phat_investment").ready()  # Important, bruh
    redis = apps.get_app_config("phat_investment").redis_client
else:
    print("Redis client initialized in phat_investment app config")

INVESTMENT_CHOICE = [
    ("VESAF", "VESAF"),
    ("VFF", "VFF"),
    ("VMEEF", "VMEEF"),
    ("VEOF", "VEOF"),
    ("VIBF", "VIBF"),
    ("VDEF", "VDEF"),
    ("stock", "stock"),
    ("DCDE", "DCDE"),
    ("ETH", "ETH"),
    ("BTC", "BTC"),
    ("XAUt", "XAUt"),
]


class Investment(models.Model):
    date = models.DateField(default=date.today)
    investment_type = models.CharField(max_length=15, choices=INVESTMENT_CHOICE)
    amount = models.PositiveIntegerField(blank=True, default=0)

    @transaction.atomic
    def invest(self, investment_type: str, amount: int) -> None:
        """
        Invest into assets 🪙💹. Deduct balance.digital accordingly
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

    def save(self, *args, **kwargs):
        self.invest(self.investment_type, self.amount)
        super().save(*args, **kwargs)
