from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
from upstash_redis import Redis

from .models.expense import Expense
from api.serializers.expense import ExpenseSerializer

@login_required
def dashboard(request):
    #Initialize Redis
    redis = Redis.from_env()
    
    expensable = int(redis.get("expensable"))
    necessity = int(round(0.4 * expensable,-3))
    pleasure = int(round(0.1 * expensable,-3))
    rent = int(redis.get("rent"))
    vacation = int(redis.get("vacation"))
    funds =  int(redis.get("funds"))
    saving_month = int(redis.get("saving_month"))
    investment_month = int(redis.get("investment_month"))
    cashflow =  expensable - (
        necessity + pleasure + rent + vacation
        + funds + saving_month + investment_month)
    
    rendered = render_to_string("dashboard.html", {
        "balance_cash": redis.get('balance_cash')
        , "balance_digital": redis.get('balance_digital')
        , "expense_cash": redis.get('expense_cash')
        , "expense_digital": redis.get('expense_digital')
        , "expense_credit": redis.get('expense_credit')
        , "emergency_fund": redis.get('emergency_fund')
        , "sinking_fund": redis.get('sinking_fund')
        , "asset": redis.get('asset')
        , "total_debt": redis.get('total_debt')
        , "total_investment": redis.get('total_investment')
        , "last_changes": redis.get('last_changes')
        , "last_changes_log": redis.get('last_changes_log')
        , "expensable": expensable
        , "necessity": necessity
        , "pleasure": pleasure
        , "saving_month": saving_month
        , "investment_month": investment_month
        , "rent": rent
        , "vacation": vacation
        , "funds": funds
        , "cashflow" : cashflow
    })
    return HttpResponse(rendered)

@login_required
def expense(request):
    date = request.GET.get('date', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    category = request.GET.get('category', None)
    expense_origin = Expense.objects.all().order_by('-date')
    expenses = None
    if date:
        expenses = expense_origin.filter(date=date)
    elif start_date and end_date:
        expenses = expense_origin.filter(date__range=(start_date,end_date))
    elif category:
        expenses = expenses.filter(category=category)
    else:
        expenses = expense_origin
    total_cash = expenses.aggregate(total=Sum('cash'))['total'] or 0
    total_digital = expenses.aggregate(total=Sum('digital'))['total'] or 0
    total_credit = expenses.aggregate(total=Sum('credit'))['total'] or 0
    json_data = json.loads(serializers.serialize('json', expenses))
    print(type(json_data))
    print(json_data)
    try:
        return render(request, 'expense.html',
            {'json_data': json_data,
            'total_cash': total_cash,
            'total_digital': total_digital,
            'total_credit': total_credit,
            'start_date': start_date,
            'end_date': end_date,
            'date': date,
            })
    except loader.TemplateDoesNotExist:
        return HttpResponseNotFound("Expense template not found.")
