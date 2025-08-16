from django.apps import apps
from django.db import models
from django.db.models import Sum
from datetime import date,datetime
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
redis = apps.get_app_config('phat_finance').redis_client

CARD_CHOICES = [
    ('VISA Platinum', 'VISA Platinum'),
    ('VJB', 'VJB'),
]

class CreditCardPayment(models.Model):
    term = models.CharField(max_length=7,blank=False,null=False)
    amount = models.PositiveIntegerField(blank=True,default=0)
    card = models.CharField(max_length=20,choices=CARD_CHOICES,null=False, default='VISA Platinum')
    description = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return f"Credit card payment - {self.term}: {self.amount} VND💸"

    def save(self, *args, **kwargs):
        @transaction.atomic
        def pay_creditCard(amount):
            """
            Decrease digital 🏧 balance by {amount} on Redis
            """
            pipeline = redis.multi()
            pipeline.decrby("balance_digital", amount)
            pipeline.mset({
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Pay credit card 💳 bill: {amount}"
            })
            pipeline.exec()

        pay_creditCard(self.amount)
        super().save(*args, **kwargs) #Over-wrote the save() method
