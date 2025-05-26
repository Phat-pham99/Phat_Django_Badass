import sys
sys.path.append("..")

from django.contrib import admin
from django.db import transaction

from .models.investment import Investment
from .models.track_investment import TrackInvestment
from phat_finance.models.balances import Balance

#-----Start Action section-----
@transaction.atomic
def invest(modeladmin, request, queryset):
    """
    Invest into assets 🪙💹. Deduct balance.digital accordingly
    """
    investment_type = queryset[0].investment_type
    amount = queryset[0].amount
    try:
        balance, _ = Balance.objects.get_or_create()
        balance.digital -= amount
        balance.save()
        modeladmin.message_user(request, f"Successfully invest {"{:,.0f}".format(float(amount))} to {investment_type}", level='SUCCESS')
    except Exception as e:
        pass
    invest.short_description = "Invest into assets 🪙💹. Deduct balance.digital accordingly"
#-----End Action section-----

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date','investment_type','amount')
    search_fields = ('date','investment_type')
    list_filter = ('date','investment_type')
    actions = [invest]

@admin.register(TrackInvestment)
class TrackInvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'acbs', 'mio', 'total')
    list_filter = ('date', 'acbs')