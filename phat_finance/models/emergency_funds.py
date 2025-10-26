from django.apps import apps
from django.db import models
from datetime import date, datetime
from django.db import transaction
from upstash_redis import Redis
import logging
from ..enums.finance_enums import FUND_ENUM

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    print("Redis client initialized in phat_finance app config")

class EmergencyFund(models.Model):
    date = models.DateField(default=date.today)
    type = models.CharField(choices=FUND_ENUM, default="deposite")
    amount = models.PositiveIntegerField(blank=False, default=0)

    @transaction.atomic
    def fund_deposit(self, redis_client: Redis, amount: int) -> None:
        """
        Deposit money to Emergency fund 💰, fund up and balance 💵 down by amount.
        """
        pipeline = redis_client.multi()
        pipeline.decrby("balance_digital", amount)
        pipeline.incrby("emergency_fund", amount)
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Emergency fund deposited : \
                    {'{:,.0f}'.format(float(amount))}",
            }
        )
        pipeline.exec()

    @transaction.atomic
    def fund_withdraw(self, redis_client: Redis, amount: int) -> None:
        """
        Withdraw money from Emergency fund 💰, fund down and balance 💵 up by amount.
        """
        pipeline = redis_client.multi()
        pipeline.incrby("balance_digital", amount)
        pipeline.decrby("emergency_fund", amount)
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Emergency fund withdrawn : \
                    {'{:,.0f}'.format(float(amount))}",
            }
        )
        pipeline.exec()

    def save(self, *args, **kwargs):
        if self.type == "deposite":
            self.fund_deposit(redis, self.amount)
        elif self.type == "withdraw":
            self.fund_withdraw(redis, self.amount)
        super().save(*args, **kwargs)
