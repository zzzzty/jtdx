from django import forms
from .models import Teacher
from teachingtask.models import TeachingTask 
from student.models import Student
from attendance.models import Attendance
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import auth
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from django.contrib.admin import widgets
from datetimepicker.widgets import DateTimePicker

class TeacherLoginForm(forms.Form):
    username = forms.CharField(label='姓名' \
        ,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码' \
        ,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名密码不对')
        else:
            self.cleaned_data['user'] = user
        try:
            captcha_x = self.cleaned_data['captcha']
        except:
            raise forms.ValidationError('验证码错误')
        return self.cleaned_data

class RegTeacherForm(forms.Form):
    username = forms.CharField(label = "用户名" \
        ,max_length=30,min_length=3 \
        ,required=True,widget=forms.TextInput(attrs= \
            {'class':'form-control','placeholder':'yourname'}))

    email = forms.EmailField(label = "邮箱",widget=forms.EmailInput(attrs= \
        {'class':'form-control','placeholder':'jane.doe@example.com'}))

    password =forms.CharField(label = "密码",min_length=6 \
        ,widget=forms.PasswordInput( attrs = {'class':'form-control' \
            ,'placeholder':'密码长度最小为6'}))
    password_again=forms.CharField(label = "确认密码",min_length=6 \
        ,widget=forms.PasswordInput( attrs = {'class':'form-control' \
            ,'placeholder':'在输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码输入的不同')
        return password_again


# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['student','attendance_time','attendance_reason']
#         widgets = {
#             'student':forms.Select(attrs={'class':'form-control','multiple':'multiple'}),
#             }
#     def __init__(self,classes = None,**kwargs):
#         super(AttendanceForm,self).__init__(**kwargs)
#         if classes:
#             self.fields['student'].queryset = Student.objects.filter(classes = classes)

class AttendanceForm(forms.Form):
    choices = [
        ("第1节课","第1节课"),
        ("第2节课","第2节课"),
        ("第3节课","第3节课"),
        ("第4节课","第4节课"),
        ("第5节课","第5节课"),
        ("第6节课","第6节课"),
    ]
    student = forms.ModelChoiceField(queryset=None, \
        widget=forms.Select(attrs={'class':'form-control','multiple':'multiple', \
            'placeholder':'选择时间','size':'10'}))
    attendance_time = forms.CharField(label='考勤日期' \
        ,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'选择时间'}))
    select_detail = forms.ChoiceField(choices = choices)

    #attendance_reason =

    def __init__(self,classes = None ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['student'].queryset = Student.objects.filter(classes = classes )





# class IScore(forms.ModelForm):
#     class Meta:
#         model = Score
#         fields = ['score','task','student']