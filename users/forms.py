from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
# class RegisterForm(UserCreationForm):
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # self.fields['username'].help_text=None
#         for fieldname in ['username','password1','password2']:
#             self.fields[fieldname].help_text=None
            

#     class Meta:
#         model=User
#         fields=['username','email','first_name','password1','password2']

#         widgets={
#             'password1': forms.PasswordInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter password'
#             }),
#         }


class CRegisterForm(forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput,label='Passwod')
    Conform_password=forms.CharField(widget=forms.PasswordInput,label='Conform Password')
    class Meta:
        model=User
        fields=['username','password1','Conform_password','email']

    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('Conform_password')
        errors=[]
        if len(password1) < 8:
             errors.append('password must be 8 caracter')

        if (password1 and password2) and (password1!=password2):
            errors.append('password Ae Not same')

        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    def clean_email(self):
        email=self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ths email already exists')
        return email
 
        
        
 