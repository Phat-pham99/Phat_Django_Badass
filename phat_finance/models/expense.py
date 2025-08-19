from django.apps import apps
from django.db import models
from django.db.models import Sum
from datetime import date,datetime
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


redis = apps.get_app_config('phat_finance').redis_client
if redis is None:
    apps.get_app_config('phat_finance').ready() #Important, bruh
    redis = apps.get_app_config('phat_finance').redis_client
else:
    print("Redis client initialized in phat_finance app config")

USER_CHOICES = [
    ('Phat', "Phat")
]

CATEGORY_CHOICES = [
    ('food_drink 🍔🍜☕', 'food_drink 🍔🍜☕'),
    ('gas ⛽⚡🚛', 'gas ⛽⚡🚛'),
    ('dating 😘😻💌','dating 😘😻💌'),
    ('grocery 🛒🥦🥩', 'grocery 🛒🥦🥩'),
    ('medical 💊🧑‍⚕️🩺', 'medical 💊🧑‍⚕️🩺'),
    ('subscriptions💳💸🏦', 'subscriptions💳💸🏦'),
    ('utility ⚙️🪒🪠', 'utility ⚙️🪒🪠'),
    ('others🙄😏','others🙄😏'),
    ('pleasure🥳🎉🪩','pleasure🥳🎉🪩'),
    ('bikecare 🏍️🛣️🧑‍🔧','bikecare 🏍️🛣️🧑‍🔧'),
    ('insurance','insurance'),
    ('gifts🎁💌💐','gifts🎁💌💐'),
    ('donation 🧧💸🫂','donation 🧧💸🫂'),
    ('haircut 💇‍♂️💈👱','haircut 💇‍♂️💈👱')
]

class Expense(models.Model):
    date = models.DateField(default=date.today)  # Use date.today() as the default
    user = models.CharField(max_length=50,choices=USER_CHOICES,blank=True,
    null=True,default='Phat')
    cash = models.PositiveIntegerField(blank=True,default=0)
    digital = models.PositiveIntegerField(blank=True,default=0)
    credit = models.PositiveIntegerField(blank=True,default=0)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return f"{self.date} - {self.user} - {self.category} - Cash: {self.cash}"

    def save(self, *args, **kwargs):
        @transaction.atomic
        def spend(cash_amount,digital_amount, credit_amount):
            """
            Decrease cash 💶💷 or digital 🏧 balance by {_amount} on Redis when cash is spent.
            """
            pipeline = redis.multi()
            if cash_amount > 0:
                pipeline.decrby('balance_cash', cash_amount)
                pipeline.incrby('expense_cash', cash_amount)
            elif digital_amount > 0:
                pipeline.decrby('balance_digital', digital_amount)
                pipeline.incrby('expense_digital', digital_amount)
            elif credit_amount > 0:
                pipeline.incrby('expense_credit', credit_amount)
            else:
                pass
            pipeline.mset({
                "last_changes": str(datetime.now()),
                "last_changes_log": f"Money 💵 spent: \n cash: {'{:,.0f}'.format(float(cash_amount))} \
                        digital: {'{:,.0f}'.format(float(digital_amount))} \
                        credit:  {'{:,.0f}'.format(float(credit_amount))} "
                })
            pipeline.exec()

        spend(self.cash, self.digital, self.credit)
        super().save(*args, **kwargs) #Man this shit is important !
