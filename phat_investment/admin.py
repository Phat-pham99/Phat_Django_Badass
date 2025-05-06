from django.contrib import admin
from .models.track_investment import TrackInvestment

# Register your models here.
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'acbs', 'mio', 'total')
    list_filter = ('date', 'acbs')

admin.site.register(TrackInvestment, InvestmentAdmin)