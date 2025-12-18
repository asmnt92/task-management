from django.urls import path
from tasks.views import manager_dashboard, employee_dashboard,create_task,update_task,view_task,delete_task,task_detail,dashboard,Test_class,TaskCreate,UpdateTask

urlpatterns = [
    path('manager-dashboard/', manager_dashboard,name='manager-dashboard'),
    path('user-dashboard/', employee_dashboard),
    # path('create-task/', create_task,name='create-task'),
    path('create-task/', TaskCreate.as_view(),name='create-task'),
    path('view-task/',view_task,name='view-task'),
    path('task-detail/<int:task_id>/',task_detail,name='task-detail'),
    # path('update-task/<int:id>/',update_task,name='update-task'),
    path('update-task/<int:id>/',UpdateTask.as_view(),name='update-task'),
    path('delete-task/<int:id>',delete_task,name='delete-task'),
    path('dashboard/', dashboard, name='dashboard'),

    # practice for knowledge
    path('test/',Test_class.as_view(d ='try to access')),
    # path('abc/',abc),
]

