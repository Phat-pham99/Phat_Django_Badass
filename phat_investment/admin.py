import sys
sys.path.append("..")

from django.contrib import admin

from .models.investment import Investment
from .models.track_investment import TrackInvestment
from .models.dividend import Dividend_new

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date','investment_type','amount')
    search_fields = ('date','investment_type')
    list_filter = ('date','investment_type')

@admin.register(TrackInvestment)
class TrackInvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'acbs', 'mio', 'dragon', 'ssi', 'idle_cash', 'crypto',  'total')
    list_filter = ('date',)

@admin.register(Dividend_new)
class DividendAdmin(admin.ModelAdmin):
    list_display = ('secCd','rightType','ownQty','recAmt','recQty','ownerFixDate','expectedExcDate')
    list_filter = ('ownerFixDate','rightType')