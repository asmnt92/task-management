from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm,TaskDetailModelForm 
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import datetime,timedelta
from django.db.models import Count,Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from users.views import is_admin




# Create your views here.
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager,login_url='no-permission')
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

@user_passes_test(is_employee,login_url='no-permission')
def employee_dashboard(request):
    
    return render(request, "dashboard/user-dashboard.html")



@login_required
@permission_required('tasks.add_task',login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form=TaskDetailModelForm()  # For GET

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)
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

@login_required
@permission_required('tasks.change_task',login_url='no-permission')
def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    task_detail_form=TaskDetailModelForm()
    
    if TaskDetail.objects.filter(task=task).exists():
        task_detail_form=TaskDetailModelForm(instance=task.details)
        
    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)
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

@login_required
@permission_required('tasks.delete_task',login_url='no-permission')
def delete_task(request,id):
    if request.method=='POST':
        t=Task.objects.get(id=id)
        t.delete()

        messages.success(request,'Task Delete Successfuly')
        return redirect('manager-dashboard')
    
    else:
        messages.error(request,'Somethings went wrong')
        return redirect('manager-dashboard')

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_task(request):
    tasks = Task.objects.select_related('project').prefetch_related('assigned_to').all()
    return render(request, 'show_task.html', {'tasks': tasks})

@login_required
@permission_required('tasks.view_taskdetail', login_url='no-permission')
def task_detail(request,task_id):
    task=Task.objects.select_related('details').prefetch_related('assigned_to').get(id=task_id)
    
    if request.method=='POST':
        new_status=request.POST.get('task_status')
        
        if new_status in dict(task.STATUS_CHOICES).keys():
            task.status=new_status
            task.is_completed= new_status == 'COMPLETED'
            task.save()


    return render(request,'dashboard/task-detail.html',{'task':task})






@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    return redirect('no-permission')



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
