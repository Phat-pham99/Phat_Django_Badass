from django.shortcuts import render
# import sys

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
import json

# sys.path.append("..")
from .models.track_investment import TrackInvestment
from .models.investment import Investment
from forms.forms import DateFilterForm

@login_required
@csrf_exempt
def portfolio_history(request):
    """
    Render the portfolio page with investment data.
    """
    date_filter = DateFilterForm(request.POST)
    start_date_form = None
    end_date_form = None
    if request.method == "POST":
        if date_filter.is_valid():
            start_date_form = date_filter.cleaned_data['start_date']
            end_date_form = date_filter.cleaned_data['end_date']
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    # portfolio_history = TrackInvestment.objects.all().order_by('-date')
    portfolio = None
    if start_date_form and end_date_form:
        portfolio = TrackInvestment.objects.all().order_by('-date').filter(date__range=(start_date_form,end_date_form))
    elif start_date and end_date:
        portfolio = TrackInvestment.objects.all().order_by('-date').filter(date__range=(start_date,end_date))
    else:
        portfolio = TrackInvestment.objects.all().order_by('-date')

    json_data = json.loads(serializers.serialize('json', portfolio))
    portfolio_data = {'date':[],'total':[],'acbs':[],'mio':[],'dragon':[],'ssi':[],'idle_cash':[],'crypto':[]}
    for item in json_data:
        portfolio_data['date'].append(item['fields']['date'])
        portfolio_data['total'].append(item['fields']['total'])
        portfolio_data['acbs'].append(item['fields']['acbs'])
        portfolio_data['mio'].append(item['fields']['mio'])
        portfolio_data['dragon'].append(item['fields']['dragon'])
        portfolio_data['ssi'].append(item['fields']['ssi'])
        portfolio_data['idle_cash'].append(item['fields']['idle_cash'])
        portfolio_data['crypto'].append(item['fields']['crypto'])

    rendered = render_to_string("portfolio.html", {
        "portfolio_data": portfolio_data,
        "date_filter": date_filter,
    })

    return HttpResponse(rendered)
