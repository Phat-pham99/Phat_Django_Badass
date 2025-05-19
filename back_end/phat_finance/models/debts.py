from django.db import models
from django.utils import timezone

DEBT_CHOICES = [
    ('debt','debt'),
    ('lend','lend')
]

class Debts(models.Model):
    start_date = models.DateField(auto_now=True,blank=False)
    due_date = models.DateField(blank=True)
    type = models.CharField(choices=DEBT_CHOICES,default='lend')
    amount = models.PositiveIntegerField(blank=False,default=0)
    client = models.CharField(max_length=30,blank=True)
    total = models.PositiveIntegerField(blank=False,default=0)

    def save(self, *args, **kwargs):
        self.total = self.amount if self.type == "lend" else -1*self.amount
        super().save(*args, **kwargs)