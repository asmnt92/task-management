from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import datetime,timedelta
from django.db.models import Count




# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


# def test(request):
#     names = ["Mahmud", "Ahamed", "John", "Mr. X"]
#     count = 0
#     for name in names:
#         count += 1
#     context = {
#         "names": names,
#         "age": 23,
#         "count": count
#     }
#     return render(request, 'test.html', context)


def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm()  # For GET

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            """ For Model Form Data """
            form.save()

            return render(request, 'task_form.html', {"form": form, "message": "task added successfully"})

    context = {"form": form}
    return render(request, "task_form.html", context)


def view_task(request):
    # # tasks=Task.objects.all()
    # # retrive specific data
    # # task_3=Task.objects.get(id=3)
    # tasks=Task.objects.filter(title__icontains='agreement')
    # # tasks=Task.objects.filter(due_date=date.today())
    # # tasks=TaskDetail.objects.filter(task.title__icontains='agreement')
    # tasks=Task.objects.select_related('details').all()
    # tasks=TaskDetail.objects.select_related('task').all()
    # tasks=Employee.objects.prefetch_related('tasks').all()
    task_count=Task.objects.aggregate(c=Count('title'))
    e=Employee.objects.prefetch_related('tasks').all()
    for emp in e:
        print(emp)
        for t in emp.tasks.all():
            print(f'>>>> {t}')
    
    return render(request,'show_task.html',{'tasks':task_count})



def tr(request):
    # t= Task.objects.prefetch_related('assigned_to').all()
    # e= Employee.objects.prefetch_related('tasks').all()
    # t=Task.objects.filter(due_date=date.today())
    # t=Task.objects.select_related('details').exclude(details__priority='L')
    # e=Employee.objects.prefetch_related('tasks').all().annotate(t=Count('tasks'))
    # t=Task.objects.all()
    # p=Project.objects.annotate(t=Count('task'))
    # d=datetime.today()-timedelta(days=7)
    # print(d)
    # t= Task.objects.filter(due_date__lte=d,is_completed=False)
    # e=Employee.objects.annotate(total=Count('tasks')).order_by('-total')
    t=Task.objects.exclude(status="PENDING")

    
    return render(request,'index.html',{'tasks':t})
