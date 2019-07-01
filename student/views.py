
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Student
from .forms import StudentLoginForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
# Create your views here.
def student_home(request):
    if request.method == 'POST':
        teacherloginform = StudentLoginForm(request.POST)
        if teacherloginform.is_valid():
            try:
                username = teacherloginform.cleaned_data['username']+"_" \
                            +teacherloginform.cleaned_data['student_num']
                User.objects.get(username = username).student.is_student
                #auth.logout(request)
                user = teacherloginform.cleaned_data['user']
                auth.login(request,user)
                return render(request,'student/student_home.html',{})
            except:
                context = {}
                context['message'] = '不是'
                context['teacherloginform'] = teacherloginform
                return render(request,'student/student_home.html',context)

    else:
        teacherloginform = StudentLoginForm()
    context={}
    context['teacherloginform'] = teacherloginform
    return render(request,'student/student_home.html',context)


def rate_teacher(request):

    return render(request,'student/rateteacher.html',{})


