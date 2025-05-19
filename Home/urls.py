from django.urls import path, include
from . import Views

app_name = 'Home'

urlpatterns = [
    path('', Views.home.landing ,name='home'),
    path('about', Views.home.about ,name='about'),
    path('home/', Views.home.home ,name='home'),
    # Add more URL patterns for myapp1 here
]