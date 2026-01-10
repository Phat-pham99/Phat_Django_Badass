from django.contrib import admin
from django.urls import path
from django.views import debug
from django.urls import include, path
from django.views.generic.base import TemplateView

from Home.views import home as Homepage
from phat_finance.views.expense import expense
from phat_finance.views.dashboard import dashboard
from phat_investment.views import portfolio_history

urlpatterns = [
    path("", Homepage, name="home"),
    path("phat_finance/dashboard", dashboard, name="index"),
    path("phat_finance/expense", expense, name="index"),
    path("phat_investment/portfolio", portfolio_history, name="portfolio_history"),
    path("admin/", admin.site.urls),
]
