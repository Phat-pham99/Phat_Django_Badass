
from django.db import models
from datetime import date,datetime
from django.db import transaction
from upstash_redis import Redis

#Initialize Redis
redis = Redis.from_env()

IN_OUTCHOICES = [
    ("IN","IN"),
    ("OUT","OUT"),
    ("SALARY","SALARY"),
]

class InOutFlow(models.Model):
    date = models.DateField(default=date.today)  # Use date.today() as the default
    type = models.CharField(max_length=10,choices=IN_OUTCHOICES,blank=False,
    null=False,default='IN')
    amount = models.PositiveIntegerField(blank=False,default=0)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.type == "SALARY":
            """
            Digital money 💵💻 enter the system. Increase balance.digital by amount
            """
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', self.amount)
            pipeline.set('last_changes',str(datetime.now()))
            pipeline.set('last_changes_log',f"Salary added: {'{:,.0f}'.format(float(self.amount))}")
            pipeline.exec()
        super().save(*args, **kwargs) #Man this shit is important !
