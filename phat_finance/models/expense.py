from django.db import models
from django.db.models import Sum
from datetime import date,datetime
from django.db import transaction
from upstash_redis import Redis

USER_CHOICES = [
    ('Phat', "Phat")
]

CATEGORY_CHOICES = [
    ('food&drinks', 'food&drinks'),
    ('gas', 'gas'),
    ('dating','dating'),
    ('grocery', 'grocery'),
    ('medical', 'medical'),
    ('subscriptions', 'subscriptions'),
    ('utility', 'utility'),
    ('others','others'),
    ('pleasure','pleasure'),
    ('inbody','inbody'),
    ('bikecare','bikecare'),
    ('insurance','insurance'),
    ('gift','gift'),
    ('donation','donation'),
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
        #Initialize Redis
        redis = Redis.from_env()

        @transaction.atomic
        def spend(cash_amount,digital_amount, credit_amount):
            """
            Updates the cash 💶💷 and digital 🏧 balance in Redis when cash is spent.
            """
            pipeline = redis.multi()
            if cash_amount > 0:
                pipeline.decrby('balance_cash', cash_amount)
            elif digital_amount > 0:
                pipeline.decrby('balance_digital', digital_amount)
            pipeline.set('last_changes', str(datetime.now()))
            pipeline.set('last_changes_log', f"Money 💵 spent: \n cash: {'{:,.0f}'.format(float(cash_amount))} \
                        digital: {'{:,.0f}'.format(float(digital_amount))} \
                        credit:  {'{:,.0f}'.format(float(credit_amount))} ")
            pipeline.exec()

        spend(self.cash, self.digital, self.credit)
        super().save(*args, **kwargs) #Man this shit is important !
