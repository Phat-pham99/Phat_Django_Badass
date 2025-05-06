from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from .total_expenses import TotalExpenses

USER_CHOICES = [
    ('ph', "Phat")
]

CATEGORY_CHOICES = [
    ('FD', 'Food & drinks'),
    ('G', 'Gas'),
    ('Gr', 'Grocery'),
    ('Md', 'Medical'),
    ('Sc', 'Subscription'),
    ('Ut', 'Utility'),
]

class Expenses(models.Model):
    date = models.DateField(auto_now=True)
    user = models.CharField(max_length=50,choices=USER_CHOICES,default='ph')
    cash = models.PositiveIntegerField(blank=True,default=0)
    digital = models.PositiveIntegerField(blank=True,default=0)
    credit = models.PositiveIntegerField(blank=True,default=0)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.date} - {self.user} - {self.category} - Cash: {self.cash}"

#        result['total_cash'] = cls.objects.aggregate(total_cash=Sum('cash'))
    @classmethod
    def get_total(cls):
        result = {}
        """Calculates the total cash spent across all records."""
        result['total_cash'] = cls.objects.aggregate(total_cash=Sum('cash')).get('total_cash')
        result['total_digital'] = cls.objects.aggregate(total_digital=Sum('digital')).get('total_digital')
        result['total_credit'] = cls.objects.aggregate(total_credit=Sum('credit')).get('total_credit')
        print("result",result)
        return result or 0  # Returns 0 if there are no records
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #Man this shit is important !
        result = self.get_total()
        total_expense = TotalExpenses()
        total_expense.total_cash = result['total_cash']
        total_expense.total_digital = result['total_digital']
        total_expense.total_credit = result['total_credit']
        total_expense.save()