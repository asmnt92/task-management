from django.shortcuts import render,redirect
from users.forms import CRegisterForm,AssignRoleForm,CreateGroupForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch

# Create your views here.
def registation(request):
    form=CRegisterForm()
    if request.method=='POST':
        form=CRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active=False
            user.save()

            return redirect('users:lg')
            
    return render(request,'registation/sign_up.html',{'form':form})

def login1(request):
    if request.method=='POST':
        u=request.POST.get('username',None)
        p=request.POST.get('password',None)

        user=authenticate(request=request,username=u,password=p)
        if user:
            login(request,user)
            re=request.GET.get('next')
            return redirect(re)
    return render(request,'registation/login.html')


def activate_user(request,id,token):
    try:
        user=User.objects.get(id=id)
        if default_token_generator.check_token(user,token):
            if not user.is_active:
                user.is_active=True
                user.save()
            return redirect('users:lg')
        else:
            return HttpResponse('Invalid User and Token')
        
    except Exception as e:
        return HttpResponse(f"invalid user")
    

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users=User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name=user.all_groups[0].name

        else:
            user.group_name='No Group Assigned'
 
    return render(request,'admin/dashboard.html',{'users':users})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    form=AssignRoleForm()
    user=User.objects.get(id=user_id)
    if request.method=='POST':
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            return redirect('users:admin-dashboard')
        
    return render(request,'admin/assign_role.html',{'form':form})

# def create_group(request):
#     form=CreateGroupForm()
#     if request.method=='POST':
#         form=CreateGroupForm(request.POST)
#         if form.is_valid():
#             group=form.save()


#     return render(request,'admin/create_group.html',{'form':form})
           
@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('users:create-group')

    return render(request, 'admin/create_group.html', {'form': form})

        
@user_passes_test(is_admin,login_url='no-permission')
def show_group(request):
    groups=Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/group_list.html',{'groups':groups})

@login_required(login_url='users:lg')
def sign_out(request):
    logout(request)

    return redirect('users:lg')

