from django.apps import apps
from django.db import models
from datetime import date, datetime
from django.db import transaction
import logging
from ..enums.finance_enums import ASSET_TRANSAC_ENUM

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    print("Redis client initialized in phat_finance app config")

class Assets(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=20, blank=True)
    price = models.PositiveIntegerField(blank=True, default=0)
    amount = models.FloatField(blank=True, default=0)
    transac_type = models.CharField(choices=ASSET_TRANSAC_ENUM, max_length=10, blank=True)

    @transaction.atomic
    def buy_asset(self, amount: int, bought_price: int) -> None:
        """
        Buy asset, increase balance.digital by amount * bought_price
        """
        pipeline = redis.multi()
        pipeline.incrby("assets", amount * bought_price)
        pipeline.decrby("balance_digital", amount * bought_price)
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Asset bought: {self.name} \
                    {'{:,.0f}'.format(float(amount * bought_price))}",
            }
        )
        pipeline.exec()

    @transaction.atomic
    def sell_asset(self, amount: int, sold_price: int) -> None:
        """
        Buy asset, increase balance.digital by amount * sold_price
        """
        pipeline = redis.multi()
        pipeline.decrby("assets", amount * sold_price)
        pipeline.incrby("balance_digital", amount * sold_price)
        pipeline.mset(
            {
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Asset sold: {self.name} \
                    {'{:,.0f}'.format(float(amount * sold_price))}",
            }
        )
        pipeline.exec()

    def save(self, *args, **kwargs) -> None:
        if self.transac_type == "buy":
            self.buy_asset(self.amount, self.price)
        elif self.transac_type == "sell":
            self.sell_asset(self.amount, self.price)
        super().save(*args, **kwargs)
