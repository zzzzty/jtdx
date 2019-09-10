
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Student
from teacher.models import Teacher
from course.models import Course
from .forms import StudentLoginForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from teachingtask.models import TeachingTask,Semester
from django.contrib.auth.decorators import login_required,permission_required
from tevaluation.models import Tevaluation,Evalution_score
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
def rate_teacher(request,teacherpk,coursepk):
    evaluations = Tevaluation.objects.all() 
    teacher = get_object_or_404(Teacher,pk = teacherpk)
    course = get_object_or_404(Course,pk = coursepk)
    user = request.user
    classes = Student.objects.get(student=user).classes
    semester = Semester.objects.get(is_execute = True)
    #判断这个班级是否有这个课程
    task = get_object_or_404(TeachingTask,teacher=teacher,course=course, \
        classes = classes,semester=semester)
    context = {}
    context["i"] = evaluations#测评的项目
    context["teacher"] = teacher.pk
    context["course"] = task.pk
    context["semester"] = semester.pk
    return render(request,'student/rateteacher.html',context)

@login_required(login_url="/student/")
def my_teacher_list(request):
    user = request.user
    student = Student.objects.get(student=user)
    semester = Semester.objects.get(is_execute=True)
    tasks = TeachingTask.objects.filter(semester=semester,classes=student.classes)
    return render(request,'student/myteacherlist.html',{'tasks':tasks})

@login_required(login_url="/student/")
def insert_evaluation(request):
    if request.method == "POST":
        semester_pk = request.POST.get("semester")
        teacher_pk = request.POST.get("teacher")
        task_pk = request.POST.get("course")
        
        user = request.user
        student = Student.objects.get(student=user)

        print("+++++++++",student,semester_pk,teacher_pk,task_pk)

        evaluations = Tevaluation.objects.all()
        for evaluation in evaluations:
            score = request.POST.get("score_"+str(evaluation.pk))
            print(score)
            new_evaluation_score = Evalution_score()
            #save the evaluations score
        return HttpResponse("SSSSSSS")




@login_required(login_url="/student/")
def my_course(request):
    return HttpResponse("my_course")
