from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request,id):
    return HttpResponse(f'<h1 style="color:gray;font-size:2rem;text-align:center">hey mama ki obosta tomader search {id}</h1>')

def awal(request):
    return HttpResponse('hey this call awal')shdsh