from django.apps import apps
from django.db import models
from datetime import date, datetime
from django.db import transaction
from types import NoneType
import logging
from ..enums.finance_enums import IN_OUT_ENUM

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    print("Redis client initialized in phat_finance app config")

class InOutFlow(models.Model):
    date = models.DateField(default=date.today)  # Use date.today() as the default
    type = models.CharField(
        max_length=12, choices=IN_OUT_ENUM, blank=False, null=False, default="IN_DIGITAL"
    )
    amount = models.PositiveIntegerField(blank=False, default=0)

    def __str__(self):
        return (
            f"{self.date}-Tiền {self.type}-{'{:,.0f}'.format(float(self.amount))} VND"
        )

    def __in_digital(self, amount: int) -> None:
        """
        Digital money 🏧💷 enter the system. Increase balance.digital by {amount}
        """
        pipeline = redis.multi()
        pipeline.incrby("phat_finance:balance_digital", amount)
        pipeline.mset(
            {
                "phat_finance:last_changes": str(datetime.now()),
                "phat_finance:last_changes_log": f"Receive: {'{:,.0f}'.format(float(amount))} digital",
            }
        )
        pipeline.exec()

    def __in_cash(self, amount: int) -> None:
        """
        Cash money 💰️💷 enter the system. Increase balance.cash by {amount}
        """
        pipeline = redis.multi()
        pipeline.incrby("phat_finance:balance_cash", amount)
        pipeline.mset(
            {
                "phat_finance:last_changes": str(datetime.now()),
                "phat_finance:last_changes_log": f"Receive: {'{:,.0f}'.format(float(amount))} cash",
            }
        )
        pipeline.exec()

    def __out_digital(self, amount: int) -> None:
        """
        Digital money 🏧💷 leave the system. Decrease balance.digital by amount
        """
        pipeline = redis.multi()
        pipeline.decrby("phat_finance:balance_digital", amount)
        pipeline.mset(
            {
                "phat_finance:last_changes": str(datetime.now()),
                "phat_finance:last_changes_log": f"Sent: {'{:,.0f}'.format(float(amount))}",
            }
        )
        pipeline.exec()

    def __out_cash(self, amount: int) -> None:
        """
        Cash money 💰️💷 leave the system. Decrease balance.cash by amount
        """
        pipeline = redis.multi()
        pipeline.decrby("phat_finance:balance_cash", amount)
        pipeline.mset(
            {
                "phat_finance:last_changes": str(datetime.now()),
                "phat_finance:last_changes_log": f"Sent: {'{:,.0f}'.format(float(amount))} cash",
            }
        )
        pipeline.exec()

    @transaction.atomic
    def __salary_paid(self, amount: int) -> None:
        """
        Digital money 💵💻 enter the system. Increase balance.digital by amount
        """
        pipeline = redis.multi()
        pipeline.incrby("phat_finance:balance_digital", amount)
        pipeline.mset(
            {
                "phat_finance:last_changes": str(datetime.now()),
                "phat_finance:last_changes_log": f"Salary added: {'{:,.0f}'.format(float(amount))}",
            }
        )
        pipeline.exec()

    def save(self, *args, **kwargs):
        if type(self.amount) == NoneType:
            self.amount = 0
        if self.type == "SALARY 💵💻":
            self.__salary_paid(self.amount)
        elif self.type == "IN_DIGITAL":
            self.__in_digital(self.amount)
        elif self.type == "OUT_DIGITAL":
            self.__out_digital(self.amount)
        elif self.type == "IN_CASH":
            self.__in_cash(self.amount)
        elif self.type == "OUT_CASH":
            self.__out_cash(self.amount)
        super().save(*args, **kwargs)  # Man this shit is important !
