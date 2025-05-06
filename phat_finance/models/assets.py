from django.db import models

class Assets(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=20,blank=True)
    bought_price = models.PositiveIntegerField(blank=True,default=0)
    amount = models.FloatField(blank=True,default=0)