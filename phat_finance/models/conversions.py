from django.db import models
from datetime import date, datetime
from django.db import transaction
from upstash_redis import Redis

CONVERSION_CHOICES = [
    ('digital📲_cash💵','digital📲_cash💵'),
    ('cash💵_digital📲','cash💵_digital📲')
]

class Conversion(models.Model):
    date = models.DateField(auto_now=True)
    type_conversion = models.CharField(choices=CONVERSION_CHOICES,default='digital_cash')
    amount = models.PositiveIntegerField(blank=False,default=0)

    def save(self, *args, **kargs):
        #Initialize Redis
        redis = Redis.from_env()
        @transaction.atomic
        def convert(type_conversion,amount):
            """
            Convert digital 📱 -> cash 💵 and vice versa
            """
            if type_conversion == "digital📲_cash💵":
                pipeline = redis.multi()
                pipeline.incrby('balance_cash', amount)
                pipeline.decrby('balance_digital', amount)
                pipeline.set('last_changes',str(datetime.now()))
                pipeline.set('last_changes_log',f"{type_conversion} : {'{:,.0f}'.format(float(amount))}")
                pipeline.exec()
            else:
                pipeline = redis.multi()
                pipeline.incrby('balance_digital', amount)
                pipeline.decrby('balance_cash', amount)
                pipeline.set('last_changes',str(datetime.now()))
                pipeline.set('last_changes_log',f"{type_conversion} : {'{:,.0f}'.format(float(amount))}")
                pipeline.exec()

        convert(self.type_conversion, self.amount)
        super().save(*args, **kargs)
