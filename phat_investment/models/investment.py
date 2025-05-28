from django.db import models
from datetime import date, datetime
from django.db import transaction
from upstash_redis import Redis

#Initialize Redis
redis = Redis.from_env()

INVESTMENT_CHOICE =[
    ('VESAF', 'VESAF'),
    ('VFF', 'VFF'),
    ('VMEEF', 'VMEEF'),
    ('VEOF', 'VEOF'),
    ('VIBF', 'VIBF'),
    ('stock', 'stock'),
    ('DCDE', 'DCDE'),
    ('ETH', 'ETH'),
    ('BTC', 'BTC'),
    ('XAUt','XAUt')

]
# Create your models here.
class Investment(models.Model):
    date = models.DateField(default=date.today)
    investment_type = models.CharField(max_length=15,choices=INVESTMENT_CHOICE)
    amount = models.PositiveIntegerField(blank=True,default=0)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Invest into assets 🪙💹. Deduct balance.digital accordingly
        """
        pipeline = redis.multi()
        pipeline.decrby('balance_digital', self.amount)
        pipeline.set('last_changes',str(datetime.now()))
        pipeline.set('last_changes_log',f"Invest to {self.investment_type}")
        pipeline.exec()
        super().save(*args, **kwargs)
