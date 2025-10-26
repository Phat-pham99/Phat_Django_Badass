from django.db import models
from ..enums.investment_enums import DIVIDEND_TYPE_ENUM

class Dividend_new(models.Model):
    secCd = models.CharField(max_length=3)
    rightType = models.CharField(max_length=5,choices=DIVIDEND_TYPE_ENUM)
    ownQty = models.PositiveSmallIntegerField()
    recAmt = models.PositiveIntegerField()
    recQty = models.PositiveSmallIntegerField()
    ownerFixDate = models.DateField()
    expectedExcDate = models.DateField()
