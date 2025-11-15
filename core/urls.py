from django.urls import path
from .views import home,no_permission

urlpatterns = [
    # path('login2/',login2,name='login'),
    path('home/',home,name='home'),
    path('no-permission/',no_permission,name='no-permission')
]
