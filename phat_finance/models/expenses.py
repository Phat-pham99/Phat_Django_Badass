from django.db import models

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