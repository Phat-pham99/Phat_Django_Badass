from django.http import HttpResponse

def signup(request):
    return HttpResponse("<h1>This is Signup page !</h1>")