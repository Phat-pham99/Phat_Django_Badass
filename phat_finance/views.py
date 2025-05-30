from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.template import loader
from django.contrib.auth.decorators import login_required
from upstash_redis import Redis


@login_required
def index(request):
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
