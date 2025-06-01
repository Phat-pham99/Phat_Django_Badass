
from django.db import models
from datetime import date,datetime
from django.db import transaction
from upstash_redis import Redis

IN_OUTCHOICES = [
    ("IN","IN"),
    ("OUT","OUT"),
    ("SALARY 💵💻","SALARY 💵💻"),
]

class InOutFlow(models.Model):
    date = models.DateField(default=date.today)  # Use date.today() as the default
    type = models.CharField(max_length=10,
                            choices=IN_OUTCHOICES,blank=False,
                            null=False,default='IN')
    amount = models.PositiveIntegerField(blank=False,default=0)

    def save(self, *args, **kwargs):
        #Initialize Redis
        redis = Redis.from_env()

        @transaction.atomic
        def salary_paid(amount):
            """
            Digital money 💵💻 enter the system. Increase balance.digital by amount
            """
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', amount)
            pipeline.set('last_changes',str(datetime.now()))
            pipeline.set('last_changes_log',f"Salary added: {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

        if self.type == "SALARY 💵💻":
            salary_paid(self.amount)
        elif self.type == "OUT":
            pass
        super().save(*args, **kwargs) #Man this shit is important !
