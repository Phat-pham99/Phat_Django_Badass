from django.apps import apps
from django.db import models
from datetime import datetime
from django.db import transaction
from types import NoneType
import logging
from ..enums.finance_enums import CONVERSION_ENUM

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    print("Redis client initialized in phat_finance app config")

class Conversion(models.Model):
    date = models.DateField(auto_now=True)
    type_conversion = models.CharField(
        choices=CONVERSION_ENUM, default="digital_cash"
    )
    amount = models.PositiveIntegerField(blank=False, default=0)

    @transaction.atomic
    def __convert(sefl, type_conversion: str, amount: int) -> None:
        """
        Convert digital 📱 -> cash 💵 and vice versa
        """
        if type_conversion == "digital📲_cash💵":
            pipeline = redis.multi()
            pipeline.incrby("balance_cash", amount)
            pipeline.decrby("balance_digital", amount)
            pipeline.mset(
                {
                    "last_changes": str(datetime.now()),
                    "last_changes_log": f"{type_conversion} : {'{:,.0f}'.format(float(amount))}",
                }
            )
            pipeline.exec()
        else:
            pipeline = redis.multi()
            pipeline.incrby("balance_digital", amount)
            pipeline.decrby("balance_cash", amount)
            pipeline.mset(
                {
                    "last_changes": str(datetime.now()),
                    "last_changes_log": f"{type_conversion} : {'{:,.0f}'.format(float(amount))}",
                }
            )
            pipeline.exec()

    def save(self, *args, **kargs):
        if type(self.amount) == NoneType:
            self.amount = 0
        self.__convert(self.type_conversion, self.amount)
        super().save(*args, **kargs)
