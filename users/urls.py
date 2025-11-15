from django.urls import path
from users.views import registation,login1,sign_out,activate_user,admin_dashboard,assign_role,create_group,show_group

app_name = 'users'
urlpatterns = [
    path('sign-up/',registation,name='sing-up'),
    path('sign-in/',login1,name='lg'),
    path("sign-out/",sign_out, name="sign-out"),
    path('activate/<int:id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list/',show_group,name='group-list')
]
