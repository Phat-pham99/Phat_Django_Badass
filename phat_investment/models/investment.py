from django.db import models

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
    date = models.DateField(auto_now=True)
    investment_type = models.CharField(max_length=15,choices=INVESTMENT_CHOICE)
    amount = models.PositiveIntegerField(blank=True,default=0)
