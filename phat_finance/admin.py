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
from .models.balances import Balance
from .models.emergency_funds import EmergencyFund
from .models.sinking_funds import SinkingFund
from .models.in_out_flows import InOutFlow

#Initialize Redis
redis = Redis.from_env()
#
#-----Start Action section-----
@transaction.atomic
def convert(modeladmin, request, queryset):
    """
    Convert digital 📱 -> cash 💵 and vice versa
    """
    type_conversion = queryset[0].type_conversion
    convert_amount = queryset[0].amount
    try:
        if type_conversion == "digital_cash":
            pipeline = redis.multi()
            pipeline.incrby('balance_cash', convert_amount)
            pipeline.decrby('balance_digital', convert_amount)
            pipeline.exec()
            modeladmin.message_user(request, f"Successfully convert {"{:,.0f}".format(float(convert_amount))} digital -> cash", level='SUCCESS')
        else:
            pipeline = redis.multi()
            pipeline.incrby('balance_digital', convert_amount)
            pipeline.decrby('balance_cash', convert_amount)
            pipeline.exec()
            modeladmin.message_user(request, f"Successfully convert {"{:,.0f}".format(float(convert_amount))} cash -> digital", level='SUCCESS')
    except Exception as e:
        modeladmin.message_user(request,f"Error processing payment: {e}", level='ERROR')
    convert.short_description = "Convert digital 📱 -> cash 💵 and vice versa"

@transaction.atomic
def salary_paid(modeladmin, request, queryset):
    """
    Digital money 💵💻 enter the system. Increase balance.digital by amount
    """
    amount = queryset[0].placeholder
    try:
        redis.incrby('balance_digital', amount)
        modeladmin.message_user(request, f"Successfully receive salary {"{:,.0f}".format(float(amount))}, \n new balance_digital is {redis.get('balance_digital')} ", level='SUCCESS')
    except Exception as e:
        modeladmin.message_user(request,f"Error while receive salary: {e}", level='ERROR')
    salary_paid.short_description = "Digital money 💵💻 enter the system. Increase balance.digital by amount"

#-----End Action section-----
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','user','cash','digital','credit','category', 'description')
    search_fields = ('date', 'category', 'description')
    list_filter = ('date', 'category')
    ordering = ('-date',)

@admin.register(Debts)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('start_date','due_date','type','amount','client')
    readonly_fields = ['total']

@admin.register(Assets)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name','bought_price','amount')
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

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ["current_month",'expense','debt',
                    'investment','asset','cash','digital',
                    'emergency_fund','sink_fund','networth'
                    ]
    fields = [('cash','digital'),('debt','asset'),'investment',
            ('emergency_fund','sink_fund')]
    readonly_fields = ['current_month','expense','networth']