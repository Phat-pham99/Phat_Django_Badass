from django.contrib import admin
from .models.expense import Expense
from .models.debts import Debts
from .models.assets import Assets
from .models.balances import Balance
from .models.emergency_funds import EmergencyFund
from .models.sinking_funds import SinkingFund
from .models.in_out_flows import InOutFlow

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','user','cash','digital','credit','category', 'description')
    search_fields = ('date', 'category', 'description')
    list_filter = ('date', 'category')
    ordering = ('-date',)

class TotalExpensesAdmin(admin.ModelAdmin):
    readonly_fields = ('current_month','total_cash','total_digital','total_credit','total_expense')
class DebtAdmin(admin.ModelAdmin):
    list_display = ('start_date','due_date','type','amount','client')
    readonly_fields = ['total']

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name','bought_price','amount')
    readonly_fields = ['date']
class EmergencyFundAdmin(admin.ModelAdmin):
    list_display = ('date','type','amount')

class SinkingFundAdmin(admin.ModelAdmin):
    list_display = ('date','type','amount')

class InOutFlowAdmin(admin.ModelAdmin):
    list_display = ['date','placeholder','amount']

class BalanceAdmin(admin.ModelAdmin):
    list_display = ["current_month",'expense','debt',
                    'investment','asset','cash','digital',
                    'emergency_fund','sink_fund','networth'
                    ]
    fields = [('cash','digital'),('debt','asset'),'investment',
            ('emergency_fund','sink_fund')]
    readonly_fields = ['current_month','expense','networth']

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Debts,DebtAdmin)
admin.site.register(InOutFlow,InOutFlowAdmin)
admin.site.register(EmergencyFund,EmergencyFundAdmin)
admin.site.register(SinkingFund,SinkingFundAdmin)
admin.site.register(Assets,AssetAdmin)
admin.site.register (Balance, BalanceAdmin)
