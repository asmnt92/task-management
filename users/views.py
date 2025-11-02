from django.shortcuts import render,redirect
from users.forms import CRegisterForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

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
            
    return render(request,'registation/sign_up.html',{'form':form})

def login1(request):
    if request.method=='POST':
        u=request.POST.get('username',None)
        p=request.POST.get('password',None)

        user=authenticate(request=request,username=u,password=p)
        if user:
            login(request,user)
            return redirect('home')
    return render(request,'registation/login.html')


def activate_user(request,id,token):
    try:
        user=User.objects.get(id=id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('users:lg')
        else:
            return HttpResponse('Invalid User and Token')
        
    except Exception as e:
        return HttpResponse(f"invalid user")
