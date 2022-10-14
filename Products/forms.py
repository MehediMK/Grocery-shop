from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_info,Category,Product,Order


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=10,required=True)
    last_name = forms.CharField(max_length=10,required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email')



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ('profile_pic','gender','address','phone')
    

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)


class UserFLEname(forms.ModelForm):
    first_name = forms.CharField(max_length=10,required=True)
    last_name = forms.CharField(max_length=10,required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

