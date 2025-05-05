from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm,TaskDetailModelForm 
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import datetime,timedelta
from django.db.models import Count,Q
from django.contrib import messages




# Create your views here.


def manager_dashboard(request):
    # total_task=Task.objects.count()
    # completed_task=Task.objects.filter(is_completed=True).count()
    # inProgress_task=Task.objects.filter(status='IN_PROGRESS').count()
    # toDos_task=Task.objects.filter(status='PENDING').count()
    counts=Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id',filter=Q(is_completed=True)),
        inProgress_task=Count('id', filter=Q(status='IN_PROGRESS')),
        toDos_task=Count('id',filter=Q(status='PENDING'))
    )
    base_query=Task.objects.select_related('details').prefetch_related('assigned_to')
    # context={
    #     'total_task':total_task,
    #     'completed_task':completed_task,
    #     'inProgress_task':inProgress_task,
    #     'toDos_task':toDos_task,
    #     'tasks':tasks
    # }
    type=request.GET.get('type','all')


    if type =='completed':
        tasks=base_query.filter(is_completed=True)
        print(tasks)
    elif type=='inprogress':
        tasks=base_query.filter(status='IN_PROGRESS')
        print(tasks)
    elif type=='pending':
        tasks=base_query.filter(status='PENDING')
        print(tasks)

    elif type=='all':
        tasks=base_query.all()
   
    print(tasks)

    context={
        'tasks':tasks,
        'counts':counts
    }

    return render(request, "dashboard/manager-dashboard.html",context)


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
    task_form = TaskModelForm()
    task_detail_form=TaskDetailModelForm()  # For GET

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            
            task_detail = task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
           
            
            messages.success(request, "Task Created Successfully")
            return redirect('create-task')
   
    context = {
        "task_form": task_form,
        'task_detail':task_detail_form
        }
    return render(request, "task_form.html", context)


def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    task_detail_form=TaskDetailModelForm()
    
    if TaskDetail.objects.filter(task=task).exists():
        task_detail_form=TaskDetailModelForm(instance=task.details)
        
    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST)
        if TaskDetail.objects.filter(task=task).exists():
            task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            
            task_detail = task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
           
            
            messages.success(request, "Task update Successfully")
            return redirect('update-task',id)
   
    context = {
        "task_form": task_form,
        'task_detail':task_detail_form
        }
    return render(request, "task_form.html", context)


def delete_task(request,id):
    if request.method=='POST':
        t=Task.objects.get(id=id)
        t.delete()

        messages.success(request,'Task Delete Successfuly')
        return redirect('manager-dashboard')
    
    else:
        messages.error(request,'Somethings went wrong')
        return redirect('manager-dashboard')

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
    # t=Task.objects.exclude(status='COMPLETED').update(is_completed='False') # data update
    t=Task.objects.all()

    
    return render(request,'index.html',{'tasks':t})

def abc(request):
   
    
    t=Task.objects.all().order_by('-due_date')

    return render(request,'index.html',{'tasks':t})
