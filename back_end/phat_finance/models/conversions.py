from django.db import models

CONVERSION_CHOICES = [
    ('digital_cash','digital_cash'),
    ('cash_digital','cash_digital')
]

class Conversion(models.Model):
    date = models.DateField(auto_now=True)
    type_conversion = models.CharField(choices=CONVERSION_CHOICES,default='digital_cash')
    amount = models.PositiveIntegerField(blank=False,default=0)
    conversion_amount = models.IntegerField(blank=False,default=0)

    def save(self, *args, **kargs):
        self.conversion_amount = self.amount if self.type_conversion=="digital_cash" else -1*self.amount
        super().save(*args, **kargs)