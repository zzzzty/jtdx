from django import forms
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Student


class StudentLoginForm(forms.Form):
    username = forms.CharField(label='姓名' \
        ,required=True,widget=forms.TextInput(attrs={'class':'form-control','width':'100'}))
    student_num = forms.CharField(label='学号' \
        ,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码' \
        ,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        student_num = self.cleaned_data['student_num']
        newusername = username+"_"+student_num
        user = auth.authenticate(username=newusername,password=password)
        if user is None:
            raise forms.ValidationError('用户名密码不对')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data