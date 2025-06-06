from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

from .models.track_investment import TrackInvestment
from .models.investment import Investment

@login_required
def portfolio_history(request):
    """
    Render the portfolio page with investment data.
    """
    date = request.GET.get('date', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    portfolio_history = TrackInvestment.objects.all().order_by('-date')
    portfolio = None
    if start_date and end_date:
        portfolio = portfolio_history.filter(date__range=(start_date,end_date))
    else:
        portfolio = portfolio_history
        
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
    })

    return HttpResponse(rendered)
