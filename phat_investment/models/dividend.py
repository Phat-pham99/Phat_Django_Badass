from django.db import models

RIGHT_TYPE = [
    ('stock', 'stock'),
    ('cash', 'cash')
]

class Dividend(models.Model):
    secCd = models.CharField(max_length=10)
    rightType = models.CharField(max_length=10, choices=RIGHT_TYPE)
    ownQty = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(blank=True,default=0)
    ownerFixDate = models.DateField(blank=True, null=True)
    expectedExcDate = models.DateField(blank=True, null=True)