from django.http import HttpResponse,HttpResponseNotFound,Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing(request):
    return HttpResponse("<h1>Hello, world. You're at landingpage</h1>")

@login_required(redirect_field_name='next', login_url='/accounts/login/')
def home(request):
    return HttpResponse("<h1>Hello, world. You're at homepage</h1>")

def about(request):
    return HttpResponse("<h1>About</h1>")

def contact(request):
    return HttpResponse("<h1>Contact</h1>")

def custom_404(request, exception):
    return HttpResponseNotFound(render(request, '../templates/404.html'))

def custom_500(request):
    return HttpResponse(render(request, 'Home/templates/500.html'))