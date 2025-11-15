from django.apps import apps
from django.db import models
from typing import final
from datetime import datetime
from logging import Logger, getLogger
from upstash_redis import Redis
from ..enums.finance_enums import DEBT_ENUM

logger: Logger = getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    logger.info("Redis client initialized in phat_finance app config")

@final
class Debts(models.Model):
    start_date = models.DateField(auto_now=True, blank=False)
    due_date = models.DateField(blank=True)
    type = models.CharField(choices=DEBT_ENUM, default="lend")
    amount = models.PositiveIntegerField(blank=False, default=0)
    lender = models.CharField(max_length=30, blank=True)
    borrower = models.CharField(max_length=30, blank=True)

    """
    Let's say these functions are "After-effects" of the saving an object
    So you need to route these functions according to the type of debt
    """
    def __I_lend_money(self, redis_client: Redis, amount: int, borrower: str) -> None:
        """
        I Lend money to a borrower, decrease balance.digital by amount.
        """
        pipeline = redis_client.multi()
        pipeline.decrby("balance_digital", amount)
        pipeline.set("last_changes", str(datetime.now()))
        pipeline.set(
            "last_changes_log",
            f"I lent money to {borrower} : \
                    {'{:,.0f}'.format(float(amount))}",
        )
        pipeline.exec()

    def __they_pay_debt(self, redis_client: Redis, amount: int, borrower: str) -> None:
        """
        Borrower pays back debt, increase balance.digital by amount.
        """
        pipeline = redis_client.multi()
        pipeline.incrby("balance_digital", amount)
        pipeline.set("last_changes", str(datetime.now()))
        pipeline.set(
            "last_changes_log",
            f"Debt paid by {borrower} : \
                    {'{:,.0f}'.format(float(amount))}",
        )
        pipeline.exec()

    def __I_own_money(self, redis_client: Redis, amount: int, lender: str) -> None:
        """
        I borrow money to a lender, increase balance.digital by amount.
        """
        pipeline: Pipeline = redis_client.multi()
        pipeline.incrby("balance_digital", amount)
        pipeline.decrby("debts", amount)
        pipeline.set("last_changes", str(datetime.now()))
        pipeline.set(
        "last_changes_log",
        f"I borrowed money from {lender} : \
        {'{:,.0f}'.format(float(amount))}",
        )
        pipeline.exec()

    def __I_pay_debt(self, redis_client: Redis, amount: int, lender: str) -> None:
        """
        I pay back debt, decrease balance.digital by amount.
        :param amount money(int)
        :param lender person(str)
        """
        pipeline: Pipeline = redis_client.multi()
        pipeline.decrby("balance_digital", amount)
        pipeline.incrby("debts", amount)
        pipeline.set("last_changes", str(datetime.now()))
        pipeline.set(
        "last_changes_log",
        f"I paid debt to {lender} : \
        {'{:,.0f}'.format(float(amount))}",
        )
        pipeline.exec()

    def save(self, *args, **kwargs) -> None:
        if self.type == "lend" and self.lender == "Me":
            self.__I_lend_money(
                redis_client=redis,
                amount=self.amount,
                borrow=self.borrower)
        elif self.type == "debt" and self.borrower == "Me":
            self.__I_own_money(
                redis_client=redis,
                amount=self.amount,
                borrow=self.borrower)
        elif self.type == "pay" and self.borrower == "Me":
            self.__I_pay_debt(
                redis_client=redis,
                amount=self.amount,
                lender=self.lender)
        elif self.type == "pay" and self.borrower != "Me":
            self.__they_pay_debt(
                redis_client=redis,
                amount=self.amount,
                lender=self.borrower)
        else:
            logger.warn("No type and lender-borrower matched !")
        super().save(*args, **kwargs)
