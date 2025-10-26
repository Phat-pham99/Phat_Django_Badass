from django.apps import apps
from django.db import models

# from django.db.models import Sum
from datetime import date, datetime
from django.db import transaction
from types import NoneType
import logging
from ..enums.finance_enums import EXPENSE_CATEGORY_ENUM
from Home.commons.enums import USER_ENUM

logger = logging.getLogger(__name__)

redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    print("Redis client initialized in phat_finance app config")

class Expense(models.Model):
    date = models.DateField(default=date.today)  # Use date.today() as the default
    user = models.CharField(
        max_length=50, choices=USER_ENUM, blank=True, null=True, default="Phat"
    )
    cash = models.PositiveIntegerField(blank=True, default=0)
    digital = models.PositiveIntegerField(blank=True, default=0)
    credit = models.PositiveIntegerField(blank=True, default=0)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORY_ENUM)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.user} - {self.category}"

    @transaction.atomic
    def spend(self, cash_amount: int, digital_amount: int, credit_amount: int) -> None:
        """
        Decrease cash 💶💷 or digital 🏧 balance by {_amount} on Redis when cash is spent.
        """
        pipeline = redis.multi()
        if cash_amount > 0:
            pipeline.decrby("balance_cash", cash_amount)
            pipeline.incrby("expense_cash", cash_amount)
        elif digital_amount > 0:
            pipeline.decrby("balance_digital", digital_amount)
            pipeline.incrby("expense_digital", digital_amount)
        elif credit_amount > 0:
            pipeline.incrby("expense_credit", credit_amount)
        else:
            pass
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Money 💵 spent: \n cash: {'{:,.0f}'.format(float(cash_amount))}\
                    digital: {'{:,.0f}'.format(float(digital_amount))}\
                    credit:  {'{:,.0f}'.format(float(credit_amount))} ",
            }
        )
        pipeline.exec()

    def save(self, *args, **kwargs):
        if type(self.cash) == NoneType:
            self.cash = 0
        if type(self.digital) == NoneType:
            self.digital = 0
        if type(self.credit) == NoneType:
            self.credit = 0

        self.spend(self.cash, self.digital, self.credit)
        super().save(*args, **kwargs)  # Man this shit is important !
