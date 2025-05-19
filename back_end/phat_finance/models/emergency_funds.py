from django.db import models

TYPE_FUND = [
    ('deposite','deposite'),
    ('withdraw','withdraw')
]
class EmergencyFund(models.Model):
    date = models.DateField(auto_now=True)
    type = models.CharField(choices=TYPE_FUND,default='deposite')
    amount = models.PositiveIntegerField(blank=False,default=0)