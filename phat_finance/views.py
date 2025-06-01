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
    balance_cash = redis.get('balance_cash')
    balance_digital = redis.get('balance_digital')
    expense_cash = redis.get('expense_cash')
    expense_digital = redis.get('expense_digital')
    expense_credit = redis.get('expense_credit')
    emergency_fund = redis.get('emergency_fund')
    sinking_fund = redis.get('sinking_fund')
    total_investment = redis.get('total_investment')
    total_debt = redis.get('total_debt')
    last_changes = redis.get('last_changes')
    last_changes_log = redis.get('last_changes_log')

    rendered = render_to_string("dashboard.html", {
        "balance_cash": balance_cash
        , "balance_digital": balance_digital
        , "expense_cash": expense_cash
        , "expense_digital": expense_digital
        , "expense_credit": expense_credit
        , "emergency_fund": emergency_fund
        , "sinking_fund": sinking_fund
        , "total_debt": total_debt
        , "total_investment": total_investment
        , "last_changes": last_changes
        , "last_changes_log": last_changes_log
    })
    return HttpResponse(rendered)

@login_required
def expense(request):
    # expenses = Expense.objects.all().order_by('-date').filter(date="2025-05-30")
    date = request.GET.get('date', None)
    date_start = request.GET.get('date_start', None)
    date_end = request.GET.get('date_end', None)
    category = request.GET.get('category', None)
    expense_origin = Expense.objects.all().order_by('-date')
    expenses = None
    if date:
        expenses = expense_origin.filter(date=date)
    elif date_start and date_end:
        expenses = expense_origin.filter(date__range=(date_start,date_end))
    if expenses and category:
        expenses = expenses.filter(category=category)
    else:
        expenses = expense_origin
    total_cash = expenses.aggregate(total=Sum('cash'))['total'] or 0
    total_digital = expenses.aggregate(total=Sum('digital'))['total'] or 0
    total_credit = expenses.aggregate(total=Sum('credit'))['total'] or 0
    print(expense_origin)
    # print("total_cash",total_cash)
    # print("total_digital",total_digital)
    # print("total_credit",total_credit)
    json_data = json.loads(serializers.serialize('json', expenses))
    print(type(json_data))
    print(json_data)
    try:
        return render(request, 'expense.html',
            {'json_data': json_data,
            'total_cash': total_cash,
            'total_digital': total_digital,
            'total_credit': total_credit,
            })
    except loader.TemplateDoesNotExist:
        return HttpResponseNotFound("Expense template not found.")
