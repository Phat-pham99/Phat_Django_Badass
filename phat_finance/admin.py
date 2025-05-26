#Import Django libs
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.db import transaction
# Import Data models
from .models.expense import Expense
from .models.debts import Debts
from .models.assets import Assets
from .models.conversions import Conversion
from .models.balances import Balance
from .models.emergency_funds import EmergencyFund
from .models.sinking_funds import SinkingFund
from .models.in_out_flows import InOutFlow

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
        # Get or create the single Balance instance
        balance, _ = Balance.objects.get_or_create()
        if type_conversion == "digital_cash":
            balance.digital -= convert_amount
            balance.cash += convert_amount
            balance.save()
            modeladmin.message_user(request, f"Successfully convert {"{:,.0f}".format(float(convert_amount))} digital -> cash", level='SUCCESS')
        else:
            balance.digital += convert_amount
            balance.cash -= convert_amount
            balance.save()
            modeladmin.message_user(request, f"Successfully convert {"{:,.0f}".format(float(convert_amount))} cash -> digital", level='SUCCESS')
    except Exception as e:
        modeladmin.message_user(request,f"Error processing payment: {e}", level='ERROR')
    convert.short_description = "Convert digital 📱 -> cash 💵 and vice versa"

@transaction.atomic
def salary_paid(modeladmin, request, queryset):
    """
    Digital money 💵💻 enter the system. Increase balance.digital by amount
    """
    type = queryset[0]._type
    amount = queryset[0].placeholder
    try:
        # Get or create the single Balance instance
        balance, _ = Balance.objects.get_or_create()
        balance.digital += amount
        balance.save()
        modeladmin.message_user(request, f"Successfully receive salary {"{:,.0f}".format(float(amount))} ", level='SUCCESS')
    except Exception as e:
        modeladmin.message_user(request,f"Error while receive salary: {e}", level='ERROR')

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
    list_display = ['date','placeholder','amount']
    actions = [salary_paid]

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ['date','type_conversion','amount']
    readonly_fields = ['conversion_amount']
    actions = [convert]

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ["current_month",'expense','debt',
                    'investment','asset','cash','digital',
                    'emergency_fund','sink_fund','networth'
                    ]
    fields = [('cash','digital'),('debt','asset'),'investment',
            ('emergency_fund','sink_fund')]
    readonly_fields = ['current_month','expense','networth']