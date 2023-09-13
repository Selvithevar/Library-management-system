from django.contrib.auth.forms import UserCreationForm
# from .models import User
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput

class ImportBooksForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
   

class updateMemberform(forms.ModelForm):
    class Meta:
        model = Member
        # fields = ['title','author','isbn','stock']
        fields = '__all__'

class CustomUserForm(UserCreationForm):   
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())