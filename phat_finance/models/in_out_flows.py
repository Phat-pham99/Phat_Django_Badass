
from django.db import models
from datetime import date

IN_OUTCHOICES = [
    ("IN","IN"),
    ("OUT","OUT")
]

class InOutFlow(models.Model):
    date = models.DateField(default=date.today)  # Use date.today() as the default
    _type = models.CharField(max_length=5,choices=IN_OUTCHOICES,blank=False,
    null=False,default='IN')
    placeholder = models.PositiveIntegerField(blank=False,default=0)
    amount = models.PositiveIntegerField(blank=True,editable=False,default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #Man this shit is important !
        self.amount = self.placeholder if self._type == "IN" else self.placeholder * (-1)
