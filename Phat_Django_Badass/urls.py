"""
URL configuration for Phat_Django_Badass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views import debug
from django.urls import include, path
from rest_framework import routers

from api.views.Expenses import ExpenseViewSet
from api.views.Investment import InvestmentViewSet
from api.views.TrackInvestment import TrackInvestmentViewSet

router = routers.DefaultRouter()
router.register(r"expenses",ExpenseViewSet, basename="expense")
router.register(r"investment",InvestmentViewSet,basename="investment")
router.register(r'track_investment', TrackInvestmentViewSet)

urlpatterns = [
    path('', debug.default_urlconf),
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
