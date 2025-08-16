from django.apps import apps
from django.db import models
from datetime import date,datetime
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
redis = apps.get_app_config('phat_finance').redis_client

ASSET_TRANSAC = [
    ('buy','buy'),
    ('sell','sell')
]

class Assets(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=20,blank=True)
    price = models.PositiveIntegerField(blank=True,default=0)
    amount = models.FloatField(blank=True,default=0)
    transac_type = models.CharField(choices=ASSET_TRANSAC,max_length=10,blank=True)

    def save(self, *args, **kwargs):
        @transaction.atomic
        def buy_asset(amount,bought_price):
            """
            Buy asset, increase balance.digital by amount * bought_price
            """
            pipeline = redis.multi()
            pipeline.incrby('assets', amount * bought_price)
            pipeline.decrby('balance_digital', amount * bought_price)
            pipeline.mset({
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Asset bought: {self.name} \
                        {'{:,.0f}'.format(float(amount * bought_price))}"
            })
            pipeline.exec()

        @transaction.atomic
        def sell_asset(amount,sold_price):
            """
            Buy asset, increase balance.digital by amount * sold_price
            """
            pipeline = redis.multi()
            pipeline.decrby('assets', amount * sold_price)
            pipeline.incrby('balance_digital', amount * sold_price)
            pipeline.mset({
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Asset sold: {self.name} \
                        {'{:,.0f}'.format(float(amount * sold_price))}"
            })
            pipeline.exec()

        if self.transac_type == "buy":
            buy_asset(self.amount, self.price)
        elif self.transac_type == "sell":
            sell_asset(self.amount, self.price)
        super().save(*args, **kwargs)
