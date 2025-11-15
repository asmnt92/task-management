from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
import re
from tasks.forms import StyledFormMixin
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


class CRegisterForm(StyledFormMixin,forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'id':'password'}),label='Passwod')
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'id':'confirm_password'}),label='Confirm Password')
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','confirm_password']

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com' }),
            'password1':forms.PasswordInput(attrs={'placeholder': 'Password' }),
            'confirm_password':forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            }

    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('confirm_password')
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
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()
 
        
        
class AssignRoleForm(StyledFormMixin,forms.Form):
    role=forms.ModelChoiceField(queryset=Group.objects.all(),empty_label='Select a Role')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()



# class CreateGroupForm(StyledFormMixin ,forms.ModelForm):
#     permission=forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#         label='Assign Permissions'
#     )
#     class Meta:
#         model=Group
#         fields=['name','permissions']

#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.apply_styled_widgets()

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
    queryset=Permission.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False,
    label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()