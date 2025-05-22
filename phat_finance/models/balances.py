from django.db import models
from datetime import date
from .debts import Debts
from phat_investment.models.investment import Investment
from phat_finance.models.in_out_flows import InOutFlow
from .assets import Assets
from .emergency_funds import EmergencyFund
from .sinking_funds import SinkingFund


class BalanceManager(models.Manager):
    def add(self,balance,cash,digital):
        if cash:
            balance.cash = balance.cash + cash
        if digital:
            balance.digital = balance.digital + digital
        balance.save()
        return balance

    def minus(self,balance,cash,digital):
        if cash:
            balance.cash = balance.cash - cash
        if digital:
            balance.digital = balance.digital - digital
        balance.save()
        return balance

    # @classmethod
    def salary_paid(self,amount):
    # Yeah I know this is some shitty codes, but I will try to improve overtime
        balance, _ = self.get_or_create()
        self.add(balance,0,amount)
        InOutFlow_obj = InOutFlow.objects.create(_type="IN",placeholder=amount)
        InOutFlow_obj.save()

    def invest(self,date,investment_type,amount):
        balance, _ = self.get_or_create(self)
        self.minus(balance,0,amount)
        Investment_obj = Investment.objects.create(date=date,
                        investment_type=investment_type,
                        amount=amount
                        )
        Investment_obj.save()


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
