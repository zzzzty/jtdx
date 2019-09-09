
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Student
from .forms import StudentLoginForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from teachingtask.models import TeachingTask,Semester
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.
def student_home(request):
    if request.method == 'GET':
        teacherloginform = StudentLoginForm()
        if request.user.username =="":
            context={}
            context['teacherloginform'] = teacherloginform
            semester = Semester.objects.filter(is_execute=True)[0]
            context['semester'] = semester
            return render(request,'student/student_home.html',context)
        else:
            try:
                User.objects.get(username = request.user).students.is_student
                return render(request,'student/student_home.html',{})
            except:
                User.objects.get(username = request.user).teachers.is_teacher
                return render(request,'teacher/teacher_home.html',{})
            else:
                return HttpResponse("不知道为什么，")
    else:
        teacherloginform = StudentLoginForm(request.POST)
        if teacherloginform.is_valid():
            try:
                username = teacherloginform.cleaned_data['username']+"_" \
                            +teacherloginform.cleaned_data['student_num']
                User.objects.get(username = username).students.is_student
                user = teacherloginform.cleaned_data['user']
                auth.login(request,user)
                return render(request,'student/student_home.html',{})
            except:
                context = {}
                semester = Semester.objects.filter(is_execute=True)[0]
                context['semester'] = semester
                context['message'] = '不是'
                context['teacherloginform'] = teacherloginform
                return render(request,'student/student_home.html',context)

    context={}
    semester = Semester.objects.filter(is_execute=True)[0]
    context['semester'] = semester
    context['teacherloginform'] = teacherloginform

    return render(request,'student/student_home.html',context)

@login_required(login_url="/student/")
def rate_teacher(request):
    i = [i for i in range(10)]
    context = {}
    context["i"] = i
    return render(request,'student/rateteacher.html',context)

@login_required(login_url="/student/")
def my_course(request):
    return HttpResponse("my_course")
