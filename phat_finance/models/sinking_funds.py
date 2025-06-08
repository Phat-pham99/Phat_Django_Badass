from django.db import models
from datetime import date,datetime
from django.db import transaction
from upstash_redis import Redis

TYPE_FUND = [
    ('deposite','deposite'),
    ('withdraw','withdraw')
]
class SinkingFund(models.Model):
    date = models.DateField(auto_now=True)
    type = models.CharField(choices=TYPE_FUND,default='deposite')
    amount = models.PositiveIntegerField(blank=False,default=0)

    def save(self, *args, **kwargs):
        #Initialize Redis
        redis = Redis.from_env()

        @transaction.atomic
        def fund_deposit(amount):
            """
            Deposit money to Sinking fund 💰, fund up and balance 💵 down by amount.
            """
            pipeline = redis.multi()
            pipeline.decrby('balance_digital', amount)
            pipeline.incrby('sinking_fund', amount)
            pipeline.set('last_changes', str(datetime.now()))
            pipeline.set('last_changes_log', f"Sinking fund deposited : \
                        {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

        @transaction.atomic
        def fund_withdraw(amount):
            """
            Withdraw money from Sinking fund 💰, fund down and balance 💵 up by amount.
            """
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', amount)
            pipeline.decrby('sinking_fund', amount)
            pipeline.set('last_changes', str(datetime.now()))
            pipeline.set('last_changes_log', f"Emergency fund withdrawn : \
                        {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

        if self.type == "deposite":
            fund_deposit(self.amount)
        elif self.type == "withdraw":
            fund_withdraw(self.amount)
        super().save(*args, **kwargs)
