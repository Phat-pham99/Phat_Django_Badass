#Import Django libs
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.db import transaction
from upstash_redis import Redis

# Import Data models
from .models.expense import Expense
from .models.debts import Debts
from .models.assets import Assets
from .models.conversions import Conversion
from .models.emergency_funds import EmergencyFund
from .models.sinking_funds import SinkingFund
from .models.in_out_flows import InOutFlow
from .models.creditcard_payment import CreditCardPayment

#Initialize Redis
redis = Redis.from_env()

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','user','cash','digital','credit','category', 'description')
    search_fields = ('date', 'category', 'description')
    list_filter = ('date', 'category')
    ordering = ('-date',)

@admin.register(Debts)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('start_date','due_date','type','amount','lender', 'borrower')

@admin.register(Assets)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name','price','amount','transac_type')
    readonly_fields = ['date']

@admin.register(EmergencyFund)
class EmergencyFundAdmin(admin.ModelAdmin):
    list_display = ('date','type','amount')

@admin.register(SinkingFund)
class SinkingFundAdmin(admin.ModelAdmin):
    list_display = ('date','type','amount')

@admin.register(InOutFlow)
class InOutFlowAdmin(admin.ModelAdmin):
    list_display = ['date','type','amount']

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ['date','type_conversion','amount']

@admin.register(CreditCardPayment)
class CreditCardPaymentAdmin(admin.ModelAdmin):
    list_display = ['term', 'amount', 'card', 'description']
    fields = [("term", "amount", "card"), "description"]
    list_filter = ('term', 'card')