from django.db import models

INVESTMENT_CHOICE =[
    ('vesaf', 'VESAF'),
    ('vff', 'VFF'),
    ('vmeef', 'VMEEF'),
    ('veof', 'VEOF'),
    ('vibf', 'VIBF'),
    ('st', 'stock'),
    ('dcde', 'DCDE'),
    ('eth', 'ETH'),
    ('btc', 'BTC'),

]
# Create your models here.
class Investment(models.Model):
    date = models.DateField(auto_now=True)
    investment_type = models.CharField(max_length=15,choices=INVESTMENT_CHOICE)
    amount = models.PositiveIntegerField(blank=True,default=0)