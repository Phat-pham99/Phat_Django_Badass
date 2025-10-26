from django.contrib import admin
from django.urls import path
from django.views import debug
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic.base import TemplateView

from api.views.Expense import ExpenseViewSet
from api.views.Investment import InvestmentViewSet
from api.views.TrackInvestment import TrackInvestmentViewSet
from api.views.TrackGym import TrackGymViewSet
from Home.views import home as Homepage
from phat_finance.views.expense import expense
from phat_finance.views.dashboard import dashboard

from phat_investment.views import portfolio_history

router = routers.DefaultRouter()
router.register(r"expense", ExpenseViewSet, basename="expense")
router.register(r"investment", InvestmentViewSet, basename="investment")
router.register(
    r"track_investment", TrackInvestmentViewSet, basename="track_investment"
)
router.register(r"track_gym", TrackGymViewSet)

urlpatterns = [
    # path('', debug.default_urlconf),
    path("", Homepage, name="home"),
    path("phat_finance/dashboard", dashboard, name="index"),
    path("phat_finance/expense", expense, name="index"),
    path("phat_investment/portfolio", portfolio_history, name="portfolio_history"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
