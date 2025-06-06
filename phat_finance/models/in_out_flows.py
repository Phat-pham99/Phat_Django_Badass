
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

    def __str__(self):
        return f"{self.date}-Tiền {self.type}-{'{:,.0f}'.format(float(self.amount))} VND"

    def save(self, *args, **kwargs):
        #Initialize Redis
        redis = Redis.from_env()

        def in_(amount):
            """
            Digital money 🏧💷 enter the system. Increase balance.digital by amount
            """
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', amount)
            pipeline.set('last_changes',str(datetime.now()))
            pipeline.set('last_changes_log',f"Receive: {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

        def out_(amount):
            """
            Digital money 🏧💷 leave the system. Decrease balance.digital by amount
            """
            pipeline = redis.multi()
            pipeline.decrby('balance_digital', amount)
            pipeline.set('last_changes',str(datetime.now()))
            pipeline.set('last_changes_log',f"Sent: {'{:,.0f}'.format(float(amount))}")
            pipeline.exec()

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
            out_(self.amount)
        else:
            in_(self.amount)
        super().save(*args, **kwargs) #Man this shit is important !
