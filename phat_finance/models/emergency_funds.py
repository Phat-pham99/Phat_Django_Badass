from django.apps import apps
from django.db import models
from datetime import date,datetime
from django.db import transaction
from types import NoneType
import logging

logger = logging.getLogger(__name__)
redis = apps.get_app_config('phat_finance').redis_client
if redis is None:
    apps.get_app_config('phat_finance').ready() #Important, bruh
    redis = apps.get_app_config('phat_finance').redis_client
else:
    print("Redis client initialized in phat_finance app config")

TYPE_FUND = [
    ('deposite','deposite'),
    ('withdraw','withdraw')
]
class EmergencyFund(models.Model):
    date = models.DateField(default=date.today)
    type = models.CharField(choices=TYPE_FUND,default='deposite')
    amount = models.PositiveIntegerField(blank=False,default=0)

    @transaction.atomic
    def fund_deposit(amount):
        """
        Deposit money to Emergency fund 💰, fund up and balance 💵 down by amount.
        """
        pipeline = redis.multi()
        pipeline.decrby('balance_digital', amount)
        pipeline.incrby('emergency_fund', amount)
        pipeline.mset({
            "last_changes": str(datetime.now()),
            "last_changes_log": f"Emergency fund deposited : \
                    {'{:,.0f}'.format(float(amount))}"
        })
        pipeline.exec()

    @transaction.atomic
    def fund_withdraw(amount):
        """
        Withdraw money from Emergency fund 💰, fund down and balance 💵 up by amount.
        """
        pipeline = redis.multi()
        pipeline.incrby('balance_digital', amount)
        pipeline.decrby('emergency_fund', amount)
        pipeline.mset({
            "last_changes": str(datetime.now()),
            "last_changes_log": f"Emergency fund withdrawn : \
                    {'{:,.0f}'.format(float(amount))}"
        })
        pipeline.exec()

    def save(self, *args, **kwargs):
        if self.type == "deposite":
            self.fund_deposit(self.amount)
        elif self.type == "withdraw":
            self.fund_withdraw(self.amount)
        super().save(*args, **kwargs)