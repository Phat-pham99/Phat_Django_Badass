from django.db import models
from datetime import date,datetime
from django.db import transaction
from upstash_redis import Redis

DEBT_CHOICES = [
    ('debt','debt'),
    ('lend','lend'),
    ('pay','pay')
]

class Debts(models.Model):
    start_date = models.DateField(auto_now=True,blank=False)
    due_date = models.DateField(blank=True)
    type = models.CharField(choices=DEBT_CHOICES,default='lend')
    amount = models.PositiveIntegerField(blank=False,default=0)
    lender = models.CharField(max_length=30,blank=True)
    borrower = models.CharField(max_length=30,blank=True)

    """
    Let's say these functions are "After-effects" of the saving an object
    So you need to route these functions according to the type of debt
    """
    def I_lend_money(self, redis_client:Redis, amount, borrower) -> None:
        """
        I Lend money to a borrower, decrease balance.digital by amount.
        """
        pipeline = redis_client.multi()
        pipeline.decrby('balance_digital', amount)
        pipeline.set('last_changes', str(datetime.now()))
        pipeline.set('last_changes_log', f"I lent money to {borrower} : \
                    {'{:,.0f}'.format(float(amount))}")
        pipeline.exec()

    def save(self, *args, **kwargs) -> None:
        #Initialize Redis
        redis = Redis.from_env()

        def they_pay_debt(amount,borrower):
            """
            Borrower pays back debt, increase balance.digital by amount.
            """
            pipeline = redis.multi()
            pipeline.decrby('balance_digital', amount)
            pipeline.set('last_changes', str(datetime.now()))
            pipeline.set('last_changes_log', f"Debt paid by {borrower} : \
                        {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()
        super().save(*args, **kwargs)

        def I_own_money(amount,lender):
            """
            I borrow money to a lender, increase balance.digital by amount.
            """
            pipeline = redis.multi()
            pipeline.decrby('balance_digital', amount)
            pipeline.incrby('debts', amount)
            pipeline.set('last_changes', str(datetime.now()))
            pipeline.set('last_changes_log', f"I borrowed money from {lender} : \
                        {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

        def I_pay_debt(amount, lender):
            """
            I pay back debt, decrease balance.digital by amount.
            """
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', amount)
            pipeline.decrby('debts', amount)
            pipeline.set('last_changes', str(datetime.now()))
            pipeline.set('last_changes_log', f"I paid debt to {lender} : \
                        {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

        if self.type == "lend" and self.lender == "Me":
            self.I_lend_money(redis, self.amount,self.borrower)
        elif self.type == "debt" and self.borrower == "Me":
            I_own_money(self.amount,self.borrower)
        elif self.type == "pay" and self.borrower == "Me":
            I_pay_debt(self.amount,self.lender)
        elif self.type == "pay" and self.borrower != "Me":
            they_pay_debt(self.amount,self.borrower)
        super().save(*args, **kwargs)