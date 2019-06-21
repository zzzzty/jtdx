from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import TeacherDevelopment
from teacher.models import Teacher

class SelectTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=None, \
        widget=forms.Select(attrs={'class':'form-control',}))

    # attendance_time = forms.CharField(label='考勤日期' \
    #     ,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'选择时间'}))
    # select_detail = forms.ChoiceField(choices = choices)
    #attendance_reason =
    def __init__(self,development = None ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(belong_to = development )

#class Course_for_taskForm(forms.Form):






