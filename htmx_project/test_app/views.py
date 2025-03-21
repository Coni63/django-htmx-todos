from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def load_message(request):
    return HttpResponse("<p>Hello, this content was loaded with HTMX!</p>")