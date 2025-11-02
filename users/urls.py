from django.urls import path
from users.views import registation,login1,activate_user

app_name = 'users'
urlpatterns = [
    path('sign-up/',registation,name='sing-up'),
    path('lg/',login1,name='lg'),
    path('activate/<int:id>/<str:token>/',activate_user),
]
