from django.db import models

from .total_expenses import TotalExpenses
from .debts import Debts
from phat_investment.models.investment import Investment
from .assets import Assets
from .emergency_funds import EmergencyFund
from .sinking_funds import SinkingFund

class Balance(models.Model):
    current_month = models.DateField(auto_now=True,
                                    verbose_name="Month/Year"
                                    )
    expense = models.OneToOneField(TotalExpenses, on_delete=models.CASCADE)
    debt = models.OneToOneField(Debts, on_delete=models.CASCADE)
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    asset = models.OneToOneField(Assets, on_delete=models.CASCADE)
    cash = models.PositiveIntegerField(blank=False,default=0)
    digital = models.PositiveIntegerField(blank=False,default=0)
    emergency_fund = models.OneToOneField(EmergencyFund, on_delete=models.CASCADE)
    sink_fund = models.OneToOneField(SinkingFund, on_delete=models.CASCADE)
    networth = models.PositiveIntegerField(blank=False,default=0,editable=False)

    def save(self, *args, **kwargs):
        self.networth = -1*self.debt + self.investment + self.asset \
            + self.cash + self.digital + self.emergency_fund + self.sink_fund
        super().save(*args, **kwargs)