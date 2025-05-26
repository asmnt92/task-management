from django.urls import path
from users.views import registation
urlpatterns = [
    path('sign-up/',registation,name='sing-up')
]
