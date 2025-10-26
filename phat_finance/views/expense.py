from django.apps import apps
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    # HttpResponseRedirect,
    HttpResponseServerError,
)
# from django.template.loader import render_to_string
# from django.contrib import messages
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

# from django.core.handlers.wsgi import WSGIRequest
# from requests.sessions import Request
from forms.forms import DateFilterForm, RedisDataForm
# from django.core.cache import cache

from datetime import datetime, timedelta

from ..models.expense import Expense
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
def expense(request):
    date_filter: DateFilterForm = DateFilterForm(request.POST)
    start_date_form: str = ""
    end_date_form: str = ""
    if request.method == "POST":
        if date_filter.is_valid():
            start_date_form: str = date_filter.cleaned_data["start_date"]
            end_date_form: str = date_filter.cleaned_data["end_date"]
    date = request.GET.get("date", None)

    start_date: str = request.GET.get("start_date", None)
    end_date: str = request.GET.get("end_date", None)
    category: str = request.GET.get("category", None)
    today: datetime = datetime.now()
    yesterday: datetime = today - timedelta(days=1)

    expense_origin = Expense.objects.filter(
        date__range=(yesterday, today)
        )

    # if cache.get("expense_origin"):
    #     expense_origin = cache.get("expense_origin")
    # else:
    #     cache.set(
    #         "expense_origin", expense_origin, timeout=60 * 5
    #     )  # Cached for 5 minutes
    expenses = None
    if date:
        expenses = Expense.objects.filter(
            date=date
            )
    elif start_date and end_date:
        expenses = Expense.objects.filter(
            date__range=(start_date, end_date)
            )
    elif start_date_form and end_date_form:
        expenses = Expense.objects.filter(
            date__range=(start_date_form, end_date_form)
            )
    elif category:
        expenses = Expense.objects.filter(
            category=category
            )
    elif start_date_form and end_date_form and category:
        expenses = Expense.objects.filter(
            category=category,
            date__range=(start_date_form, end_date_form)
            )
    else:
        expenses = expense_origin
    total_cash = sum([expense.cash for expense in expenses])
    total_digital = sum([expense.digital for expense in expenses])
    total_credit = sum([expense.credit for expense in expenses])

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