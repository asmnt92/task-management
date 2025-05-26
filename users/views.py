from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registation(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
         print(form.cleaned_data)
         p1=form.cleaned_data.get('password1')
         p2=form.cleaned_data.get('password2')
         if p1==p2:
            form.save()
            print('----------------')
    return render(request,'registation/sign_up.html',{'form':form})