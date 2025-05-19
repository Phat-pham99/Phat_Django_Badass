from django.contrib import admin
from .models.investment import Investment
from .models.track_investment import TrackInvestment
from .models.dividend import Dividend


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date','investment_type','amount')
    search_fields = ('date','investment_type')
    list_filter = ('date','investment_type')
    ordering = ('-date',)
    
class TrackInvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'acbs', 'mio','dragon','ssi','idle_cash','crypto','total')
    list_filter = ('date',)
    ordering = ('-date',)

class DividendAdmin(admin.ModelAdmin):
    list_display = ('secCd', 'rightType', 'ownQty', 'amount', 'ownerFixDate', 'expectedExcDate')
    search_fields = ('secCd', 'rightType')
    list_filter = ('secCd', 'rightType')
    ordering = ('-ownerFixDate',)

admin.site.register(TrackInvestment, TrackInvestmentAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Dividend, DividendAdmin)
