from django.db import models
from datetime import date, datetime
from django.db import transaction
from upstash_redis import Redis

#Initialize Redis
redis = Redis.from_env()

CONVERSION_CHOICES = [
    ('digital_cash','digital_cash'),
    ('cash_digital','cash_digital')
]

class Conversion(models.Model):
    date = models.DateField(auto_now=True)
    type_conversion = models.CharField(choices=CONVERSION_CHOICES,default='digital_cash')
    amount = models.PositiveIntegerField(blank=False,default=0)

    @transaction.atomic
    def save(self, *args, **kargs):
        """
        Convert digital 📱 -> cash 💵 and vice versa
        """
        if self.type_conversion == "digital_cash":
            pipeline = redis.multi()
            pipeline.incrby('balance_cash', self.amount)
            pipeline.decrby('balance_digital', self.amount)
            pipeline.set('last_changes',str(datetime.now()))
            pipeline.set('last_changes_log',f"{self.type_conversion} : {'{:,.0f}'.format(float(self.amount))}")
            pipeline.exec()
        else:
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', self.amount)
            pipeline.decrby('balance_cash', self.amount)
            pipeline.set('last_changes',str(datetime.now()))
            pipeline.set('last_changes_log',f"{self.type_conversion} : {'{:,.0f}'.format(float(self.amount))}")
            pipeline.exec()
        super().save(*args, **kargs)