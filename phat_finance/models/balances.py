#Import Django libs
from django.db import models
from django.db import transaction
# Other libs
from datetime import date
# Import Data models
from .debts import Debts
from phat_investment.models.investment import Investment
from .in_out_flows import InOutFlow
from .assets import Assets
from .emergency_funds import EmergencyFund
from .sinking_funds import SinkingFund

class BalanceManager(models.Manager):
    pass

class Balance(models.Model):
    current_month = models.DateField(auto_now=True,
                                    verbose_name="Month/Year"
                                    )
    expense = models.PositiveIntegerField(blank=False,default=0)
    debt = models.PositiveIntegerField(blank=False,default=0)
    investment = models.PositiveIntegerField(blank=False,default=0)
    asset = models.PositiveIntegerField(blank=False,default=0)
    cash = models.PositiveIntegerField(blank=False,default=0)
    digital = models.PositiveIntegerField(blank=False,default=0)
    emergency_fund = models.PositiveIntegerField(blank=False,default=0)
    sink_fund = models.PositiveIntegerField(blank=False,default=0)
    networth = models.PositiveIntegerField(blank=False,default=0,editable=False)

    objects = BalanceManager()

    def save(self, *args, **kwargs):
        self.networth = -1*self.debt + self.investment + self.asset \
            + self.cash + self.digital + self.emergency_fund + self.sink_fund
        super().save(*args, **kwargs)
