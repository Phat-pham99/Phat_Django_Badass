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
    total_expense = redis.get('total_expense')
    emergency_fund = redis.get('emergency_fund')
    sinking_fund = redis.get('sinking_fund')
    total_investment = redis.get('total_investment')
    total_debt = redis.get('total_debt')
    last_changes = redis.get('last_changes')
    last_changes_log = redis.get('last_changes_log')

    rendered = render_to_string("dashboard/index.html", {
        "balance_cash": '{:,.0f}'.format(float(balance_cash))
        , "balance_digital": '{:,.0f}'.format(float(balance_digital))
        , "total_expense": '{:,.0f}'.format(float(total_expense))
        , "emergency_fund": '{:,.0f}'.format(float(emergency_fund))
        , "sinking_fund": '{:,.0f}'.format(float(sinking_fund))
        , "total_debt": '{:,.0f}'.format(float(total_debt))
        , "total_investment": '{:,.0f}'.format(float(total_investment))
        , "last_changes": last_changes
        , "last_changes_log": last_changes_log
    })
    return HttpResponse(rendered)

@login_required
def expense(request):
    # expenses = Expense.objects.all().order_by('-date').filter(date="2025-05-30")
    expenses = Expense.objects.all().order_by('-date')
    json_data = json.loads(serializers.serialize('json', expenses))
    print(type(json_data))
    print(json_data)
    try:
        # rendered = loader.get_template("expenses/index.html").render()
        return render(request, 'expenses/index.html', {'json_data': json_data})
        # return HttpResponse(rendered)
    except loader.TemplateDoesNotExist:
        return HttpResponseNotFound("Expense template not found.")