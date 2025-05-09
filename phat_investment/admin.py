from django.contrib import admin
from .models.investment import Investment
from .models.track_investment import TrackInvestment

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date','investment_type','amount')
    search_fields = ('date','investment_type')
    list_filter = ('date','investment_type')
    
class TrackInvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'acbs', 'mio', 'total')
    list_filter = ('date', 'acbs')

admin.site.register(TrackInvestment, TrackInvestmentAdmin)
admin.site.register(Investment, InvestmentAdmin)
