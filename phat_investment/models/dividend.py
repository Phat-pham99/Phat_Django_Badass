from django.db import models

DIVIDEND_TYPE=[
    ('cash','cash'),
    ('stock','stock')
]

class Dividend_new(models.Model):
    secCd = models.CharField(max_length=3)
    rightType = models.CharField(max_length=5,choices=DIVIDEND_TYPE)
    ownQty = models.PositiveSmallIntegerField()
    recAmt = models.PositiveIntegerField()
    recQty = models.PositiveSmallIntegerField()
    ownerFixDate = models.DateField()
    expectedExcDate = models.DateField()
