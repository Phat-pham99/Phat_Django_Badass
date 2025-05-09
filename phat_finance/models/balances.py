from django.db import models
from .debts import Debts
from phat_investment.models.investment import Investment
from .assets import Assets
from .emergency_funds import EmergencyFund
from .sinking_funds import SinkingFund

class Balance(models.Model):
    current_month = models.DateField(auto_now=True,
                                    verbose_name="Month/Year"
                                    )
    expense = models.PositiveIntegerField(blank=False,default=0)
    debt = models.OneToOneField(Debts, on_delete=models.CASCADE)
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    asset = models.OneToOneField(Assets, on_delete=models.CASCADE)
    cash = models.PositiveIntegerField(blank=False,default=0)
    digital = models.PositiveIntegerField(blank=False,default=0)
    emergency_fund = models.OneToOneField(EmergencyFund, on_delete=models.CASCADE)
    sink_fund = models.OneToOneField(SinkingFund, on_delete=models.CASCADE)
    networth = models.PositiveIntegerField(blank=False,default=0,editable=False)

    def save(self, *args, **kwargs):
        self.expense_id = self.expense.id
        self.debt_id = self.debt.id
        self.investment_id = self.investment.id
        self.asset_id = self.asset.id
        self.emergency_fund_id = self.emergency_fund.id
        self.sink_fund_id = self.sink_fund.id
        self.networth = -1*self.debt.amount + self.investment.amount + self.asset.amount \
            + self.cash + self.digital + self.emergency_fund.amount + self.sink_fund.amount
        super().save(*args, **kwargs)
