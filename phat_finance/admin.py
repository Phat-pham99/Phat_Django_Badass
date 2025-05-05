from django.contrib import admin
from .models.expenses import Expenses

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date','user','cash','digital','credit','category', 'description')
    search_fields = ('date', 'category')
    list_filter = ('date', 'category')

admin.site.register(Expenses, ExpenseAdmin)