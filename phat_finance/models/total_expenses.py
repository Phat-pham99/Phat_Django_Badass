from django.db import models

class TotalExpenses(models.Model):
    current_month = models.DateField(auto_now=True,
                                    verbose_name="Month/Year"
                                    )
    total_cash = models.PositiveIntegerField(blank=True,default=0)
    total_digital = models.PositiveIntegerField(blank=True,default=0)
    total_credit = models.PositiveIntegerField(blank=True,default=0)
    total_expense = models.PositiveIntegerField(blank=True,default=0)