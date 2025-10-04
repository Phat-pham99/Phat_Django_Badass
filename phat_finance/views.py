from django.apps import apps
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from forms.forms import DateFilterForm
from django.core.cache import cache

from .models.expense import Expense
import logging

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    print("Redis client initialized in phat_finance app config")


@login_required(login_url="/admin/login")
@csrf_exempt
def dashboard(request):
    get_values = redis.mget(
        "balance_cash",
        "balance_digital",
        "expense_cash",
        "expense_digital",
        "expense_credit",
        "emergency_fund",
        "sinking_fund",
        "assets",
        "total_debt",
        "total_investment",
        "last_changes",
        "last_changes_log",
        "budget",
        "rent",
        "vacation",
        "funds",
        "saving_month",
        "investment_month",
    )

    budget = int(get_values[12])
    necessity = int(round(0.4 * budget, -3))
    pleasure = int(round(0.1 * budget, -3))
    rent = int(get_values[13])
    vacation = int(get_values[14])
    funds = int(get_values[15])
    saving_month = int(get_values[16])
    investment_month = int(get_values[17])
    cashflow = budget - (
        necessity + pleasure + rent + vacation + funds + saving_month + investment_month
    )
    try:
        rendered = render_to_string(
            "dashboard.html",
            {
                "balance_cash": get_values[0],
                "balance_digital": get_values[1],
                "expense_cash": get_values[2],
                "expense_digital": get_values[3],
                "expense_credit": get_values[4],
                "emergency_fund": get_values[5],
                "sinking_fund": get_values[6],
                "assets": get_values[7],
                "total_debt": get_values[8],
                "total_investment": get_values[9],
                "last_changes": get_values[10],
                "last_changes_log": get_values[11],
                "expensable": necessity + pleasure,
                "necessity": necessity,
                "pleasure": pleasure,
                "saving_month": saving_month,
                "investment_month": investment_month,
                "rent": rent,
                "vacation": vacation,
                "funds": funds,
                "budget": budget,
                "cashflow": cashflow,
            },
        )
        return HttpResponse(rendered)
    except loader.TemplateDoesNotExist:
        logger.warn("Expense template not found.")
        return HttpResponseNotFound("Expense template not found.")


@login_required(login_url="/admin/login")
@csrf_exempt
def expense(request):
    date_filter = DateFilterForm(request.POST)
    start_date_form = None
    end_date_form = None
    if request.method == "POST":
        if date_filter.is_valid():
            start_date_form = date_filter.cleaned_data["start_date"]
            end_date_form = date_filter.cleaned_data["end_date"]
    date = request.GET.get("date", None)

    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)
    category = request.GET.get("category", None)
    if cache.get("expense_origin"):
        expense_origin = cache.get("expense_origin")
    else:
        expense_origin = Expense.objects.all().order_by("-date")
        cache.set(
            "expense_origin", expense_origin, timeout=60 * 5
        )  # Cached for 5 minutes
    expenses = None
    if date:
        expenses = expense_origin.filter(date=date)
    elif start_date and end_date:
        expenses = expense_origin.filter(date__range=(start_date, end_date))
    elif start_date_form and end_date_form:
        expenses = expense_origin.filter(date__range=(start_date_form, end_date_form))
    elif category:
        expenses = expense_origin.filter(category=category)
    else:
        expenses = expense_origin
    total_cash = expenses.aggregate(total=Sum("cash"))["total"] or 0
    total_digital = expenses.aggregate(total=Sum("digital"))["total"] or 0
    total_credit = expenses.aggregate(total=Sum("credit"))["total"] or 0
    json_data = json.loads(serializers.serialize("json", expenses))
    try:
        return render(
            request,
            "expense.html",
            {
                "json_data": json_data,
                "date_filter": date_filter,
                "total_cash": total_cash,
                "total_digital": total_digital,
                "total_credit": total_credit,
                "start_date": start_date,
                "end_date": end_date,
                "date": date,
            },
        )
    except loader.TemplateDoesNotExist:
        logger.warning("Expense template not found.")
        return HttpResponseNotFound("Expense template not found.")
