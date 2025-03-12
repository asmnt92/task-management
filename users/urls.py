from django.urls import path
from .views import home,awal

urlpatterns = [
    path('task/<id>', home),
    path('awal/',awal)
]
