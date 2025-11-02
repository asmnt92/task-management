from django.urls import path
from .views import login2,home

urlpatterns = [
    path('login2/',login2,name='login'),
    # path('home/',home,name='home'),
]
