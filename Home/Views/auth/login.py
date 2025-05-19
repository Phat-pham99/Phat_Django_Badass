from django.http import HttpResponse

def login(request):
    # Simulate a login process
    return HttpResponse("<h1>This is Login page !</h1>")