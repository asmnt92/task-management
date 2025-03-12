from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<h1 style="color:gray;font-size:2rem;text-align:center">hey mama ki obosta tomader</h1>')
