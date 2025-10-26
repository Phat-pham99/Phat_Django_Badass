from django.apps import apps
# from django.db.models import Sum
# from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    # HttpResponseRedirect,
    HttpResponseServerError,
)
from django.template.loader import render_to_string
from django.contrib import messages
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# from django.core import serializers
# import json

# from django.core.handlers.wsgi import WSGIRequest
from requests.sessions import Request
from forms.forms import DateFilterForm, RedisDataForm
# from django.core.cache import cache

# from datetime import datetime, timedelta

# from ..models.expense import Expense
import logging

logger = logging.getLogger(__name__)
redis = apps.get_app_config("phat_finance").redis_client
if redis is None:
    apps.get_app_config("phat_finance").ready()  # Important, bruh
    redis = apps.get_app_config("phat_finance").redis_client
else:
    logger.info("Redis client initialized in phat_finance app config")

@login_required(login_url="/admin/login")
@csrf_exempt
def dashboard(request: Request):
    # messages.add_message(request, messages.INFO, "Hello Bro")
    # messages.add_message(request, messages.INFO, "Hello Bro 2")
    # message_instance = messages.get_messages(request)
    # print("messages.get_messages()", message_instance)
    # print("dir(messages.get_messages())", dir(message_instance))
    # print("message_instance._prepare_messages()", message_instance._prepare_messages())
    # print("message_instance._queued_messages()", message_instance._queued_messages)
    # for item in message_instance._queued_messages:
    #   print(item.message)

    # print("dir(messages)", dir(messages))

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
        necessity + pleasure + rent + vacation
        + funds + saving_month + investment_month
    )

    redis_form: RedisDataForm = RedisDataForm(request.POST)

    if request.method == "POST":
        if redis_form.is_valid():
            redis_balance_cash:str = redis_form.cleaned_data["balance_cash"]
            # redis_balance_cash:str = redis_form.cleaned_data["balance_cash"]
            # redis_balance_cash:str = redis_form.cleaned_data["balance_cash"]
            messages.success(request, f"redis_balance_cash -> {redis_balance_cash}")
            pass
    message_instance = messages.get_messages(request)
    print("message_instance._queued_messages()", message_instance._queued_messages)
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
                "redis_form": redis_form,
                "messages": message_instance._queued_messages,
            },
        )
        if rendered:
            return HttpResponse(rendered)
        else:
            return HttpResponseServerError
    except loader.TemplateDoesNotExist:
        logger.warning("Expense template not found.")
        return HttpResponseNotFound("Expense template not found.")