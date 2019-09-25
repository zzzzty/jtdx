
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Student
from teacher.models import Teacher
from course.models import Course
from score.models import Score
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
    context["teacher"] = teacher
    context["course"] = task
    context["semester"] = semester
    return render(request,'student/rateteacher.html',context)

@login_required(login_url="/student/")
def my_teacher_list(request):
    user = request.user
    student = Student.objects.get(student=user)
    semester = Semester.objects.get(is_execute=True)
    tasks = TeachingTask.objects.filter(semester=semester,classes=student.classes)

    #教师是否被测评，构建字典存储,课程和教师为主键
    teacher_is_evaluation = []
    for task in tasks:
        #print(student,task.teacher,task.course,semester)
        en = Evalution_score.objects.filter(student=student,teacher=task.teacher, \
                    course=task.course,semester=semester).count()>0
        if en:
            teacher_is_evaluation.append(task.teacher.teacher.username)
    context = {}
    context['tasks'] = tasks
    context['teacher_is_evaluation'] = teacher_is_evaluation
    #print(teacher_is_evaluation)
    return render(request,'student/myteacherlist.html',context)

@login_required(login_url="/student/")
def insert_evaluation(request):
    if request.method == "POST":
        semester_pk = request.POST.get("semester")
        teacher_pk = request.POST.get("teacher")
        task_pk = request.POST.get("course")
        #教师是否被测评，构建字典存储
        teacher_is_evaluation = {}
        user = request.user
        student = Student.objects.get(student=user)
        print("+++++++++",student,semester_pk,teacher_pk,task_pk)
        
        evaluations = Tevaluation.objects.all()

        for evaluation in evaluations:
            score = request.POST.get("score_"+str(evaluation.pk))
            #tevaluation = get_object_or_404(Tevaluation,pk = evaluation.pk)
            teacher = get_object_or_404(Teacher,pk = teacher_pk)
            task = get_object_or_404(TeachingTask,pk = task_pk)
            semester = Semester.objects.get(is_execute = True)

            try:
                Evalution_score.objects.get(student=student,teacher=teacher, \
                    course=task.course,semester=semester,evalution=evaluation)
                is_evaluation = True
            except:
                is_evaluation = False
                new_evaluation_score = Evalution_score()
                new_evaluation_score.student = student
                new_evaluation_score.teacher = teacher
                new_evaluation_score.course = task.course
                new_evaluation_score.semester = semester
                new_evaluation_score.score = score
                new_evaluation_score.evalution = evaluation
                new_evaluation_score.save()
            print(evaluation.content,score,is_evaluation)
            
            
            #save the evaluations score
        return redirect(reverse('my_teacher'))




@login_required(login_url="/student/")
def my_course(request):
    is_semester = request.GET.get('semester')
    print(is_semester)
    user = request.user
    #
    student = Student.objects.get(student=user)
    classes = student.classes
    semester = Semester.objects.get(is_execute = True)
    if not is_semester:
        tasks = TeachingTask.objects.filter(semester = semester,classes = student.classes).order_by('semester')
    else:
        tasks = TeachingTask.objects.filter(classes = student.classes).order_by('semester')
    return render(request,'student/student_course_list.html',locals())


@login_required(login_url="/student/")
def my_scores(request):
    user = request.user
    #
    student = Student.objects.get(student=user)
    scores = Score.objects.filter(student=student).order_by('-pk','task__semester')
    
    return render(request,'student/student_score_list.html',locals())
