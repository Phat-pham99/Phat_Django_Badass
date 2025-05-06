from django.contrib import admin
from .models.expenses import Expenses
from .models.total_expenses import TotalExpenses
from .models.debts import Debts
from .models.assets import Assets
from .models.balances import Balance
from .models.emergency_funds import EmergencyFund
from .models.sinking_funds import SinkingFund
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','user','cash','digital','credit','category', 'description')
    search_fields = ('date', 'category')
    list_filter = ('date', 'category')

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

class BalanceAdmin(admin.ModelAdmin):
    fields = [('cash','digital'),('debt','asset'),'investment',
            ('emergency_fund','sink_fund')]
    readonly_fields = ['current_month','expense','networth']
admin.site.register(Expenses, ExpenseAdmin)
admin.site.register(TotalExpenses,TotalExpensesAdmin)
# admin.site.register(Debts,DebtAdmin)
# admin.site.register(EmergencyFund,EmergencyFundAdmin)
# admin.site.register(SinkingFund,SinkingFundAdmin)
# admin.site.register(Assets,AssetAdmin)
# admin.site.register (Balance, BalanceAdmin)