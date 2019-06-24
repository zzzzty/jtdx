from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Teacher
from .forms import TeacherLoginForm,RegTeacherForm,AttendanceForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from teachingtask.models import TeachingTask,Semester
from score.forms import IScore,CScore
from score.models import Score,Change_Score
from attendance.models import Attendance,AttendanceReason
from django.forms import modelformset_factory,formset_factory
from django.contrib.auth import authenticate
from student.forms import StudentLoginForm
# Create your views here.

def teacher_home(request):
    #在此是否requestuser检测是否存在用户
    if request.method == 'POST':
        teacherloginform = TeacherLoginForm(request.POST)
        if teacherloginform.is_valid():
            try:
                User.objects.get(username = teacherloginform.cleaned_data['username']). \
                                            teachers.is_teacher
                user = teacherloginform.cleaned_data['user']
                print(user)
                auth.login(request,user)
                return render(request,'teacher/teacher_home.html',{'group_master': \
                    User.objects.get(username = teacherloginform.cleaned_data['username']). \
                                            teachers.is_group_master
                    })
            except:
                context = {}
                context['message'] = '_____不是______'
                teacherloginform = TeacherLoginForm()
                context['teacherloginform'] = teacherloginform
                return render(request,'teacher/teacher_home.html',context)
        else:
            return HttpResponse("验证未能通过，这是个错误")
    else:
        if len(request.user.username)<1:
            context = {}
            context['teacherloginform'] = TeacherLoginForm()
            return render(request,'teacher/teacher_home.html',context)
        else:
            try:
                User.objects.get(username = request.user.username). \
                                                    teachers.is_teacher
                #teacherloginform = TeacherLoginForm()
                name = request.user.username
                print("___________",name)
                user = User.objects.get(username = name)#如果是个学生如何
                teacher = Teacher.objects.get(teacher = user)
                teachingtasks = TeachingTask.objects.filter(teacher=teacher)
                context = {}

                context['name'] = name
                context['teachingtasks'] = teachingtasks
                return render(request,'teacher/teacher_task.html',context)
            except:
                context = {}
                context['teacherloginform'] = StudentLoginForm()
                return render(request,'student/student_home.html',context)

def register(request):
    if request.method == 'POST':
        register_form = RegTeacherForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username,email,password)
            newteacher = Teacher()
            newteacher.teacher = user
            newteacher.is_group_master=False
            newteacher.is_teacher = True
            newteacher.save()
            user.save()
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            context = {}
            context['register_form'] = register_form
            context['message'] = '注册成功'
            return render(request,'teacher/teacher_register.html',context)
    else:
        register_form = RegTeacherForm()
    context={}
    context['register_form'] = register_form
    return render(request,'teacher/teacher_register.html',context)

from django.contrib.auth.decorators import login_required,permission_required

@login_required(login_url="/teacher/")
def teacher_task(request):
    name = request.user.username
    user = User.objects.get(username = name)
    #如果是个学生如何 使用try 方法解决
    teacher = Teacher.objects.get(teacher = user)
    #得到当前学年学期
    semester = Semester.objects.get(is_execute = True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    teachingtasks = TeachingTask.objects.filter(teacher=teacher)
    context = {}
    context['name'] = name
    context['teachingtasks'] = teachingtasks
    return render(request,'teacher/teacher_task.html',context)

from score.forms import IScore
from student.models import Student
from django.forms import formset_factory


@login_required(login_url="/teacher/")
def teacher_insert_score(request):
    #教学任务id
    taskpk = request.GET.get('taskpk')
    #判断页面
    is_input_score = request.POST.get('is_input_score',None)
    #成绩录入表单集合
    newformset = formset_factory(IScore,extra=0)
    #生成新的表单
    #如果成绩已经录入了怎么办生成的表单，没有已经录入数据的成绩
    if is_input_score is None or request.method=="GET":
        #教学任务
        task = TeachingTask.objects.get(id=int(taskpk))
        #班级
        classes = task.classes
        #学生名单
        students = Student.objects.filter(classes = classes)
        context = {}
        #构造表单集合的默认数据
        data = []
        for s in students:
            data.append({'student_username':s.student, \
                        'student':str(s.student).split('_')[0], \
                        'task':task,'score':0, \
                        'student_num':s.student_num
                        })
        context['task'] = task
        context['taskpk'] = taskpk
        context['classes'] = classes
        context['iscore']  = newformset(initial = data)
        return render(request,'teacher/teacher_score.html',context)

    #检验表单，并将数据进行存放
    else:
        context = {}
        f = newformset(request.POST,request.FILES)
        context['classes']=request.POST.get('classes')
        context['task'] = request.POST.get('task')
        context['taskpk'] = request.POST.get('taskpk')
        if f.is_valid():
            data = []
            for i in f:
                score = Score()
                score.task = TeachingTask.objects.get(id = int(context['taskpk']))
                #student 模型是User 模型的拓展
                suser = User.objects.get(username=i.cleaned_data['student_username'])
                score.student = Student.objects.get(student=suser)
                score.score = i.cleaned_data['score']
                if Score.objects.filter(task=score.task,student=score.student).exists():
                    #不能更改表单内的内容
                    i.cleaned_data['score'] = Score.objects.filter(task=score.task,student=score.student)[0].score
                    data.append({
                        'student_username':suser.username, \
                        'student':str(suser.username).split('_')[0], \
                        'task':context['task'], \
                        'score':Score.objects.filter(task=score.task,student=score.student)[0].score, \
                        'student_num':score.student.student_num, \
                        })
                # #存入成绩
                else:
                    data.append({
                        'student_username':i.cleaned_data['student_username'], \
                        'student':i.cleaned_data['student'], \
                        'task':context['task'], \
                        'score':i.cleaned_data['score'], \
                        'student_num':i.cleaned_data['student_num'] \
                        })
                    #现在是循环多次更改task数据库++++++++++++++++++++++++++++++++++
                    score.save()
                    score.task.is_input = True
                    score.task.save()
            #检验成绩
            #context['iscore'] = newformset(initial = data)
            #return render(request,'teacher/teacher_score.html',context)
            name = request.user.username
            user = User.objects.get(username = name)#如果是个学生如何
            teacher = Teacher.objects.get(teacher = user)
            teachingtasks = TeachingTask.objects.filter(teacher=teacher)
            context = {}
            context['name'] = name
            context['teachingtasks'] = teachingtasks
            return render(request,'teacher/teacher_task.html',context)
        else:
            context['iscore'] = f
            return render(request,'teacher/teacher_score.html',context)

from classes.models import Classes
@login_required(login_url="/teacher/")
def print_name(request,taskpk):
    task = get_object_or_404(TeachingTask,id = taskpk)
    students = Student.objects.filter(classes = task.classes)
    studentinfos = []
    for s in students:
        studentinfos.append(str(s.student.username).split("_"))
    context = {}
    context['students'] = studentinfos
    context['task'] =task
    #next_loop = 45 - students.count()
    next_index = []
    for i in range(students.count()+1,45,1):
        next_index.append(i)
    context['next_index'] = next_index
    return render(request,'teacher/name.html',context)

@login_required(login_url="/teacher/")
def change_score(request,taskpk):
    #the get way
    if request.method == "GET":
        task = get_object_or_404(TeachingTask,id = taskpk)
        students = Student.objects.filter(classes = task.classes)
        scores = Score.objects.filter(task = task)
        data = []
        for s in students:
            try:
                score = Score.objects.get(task=task,student=s,make_up = 1)
                try:
                    change_to = Change_Score.objects.get(changescore=score).change_to
                except:
                    change_to = score.score
                if not score.is_changed:
                    data.append({"changescore":score.pk, \
                                "task":task, \
                                "old_score":score.score, \
                                "student_num":str(s).split("_")[1], \
                                "student":str(s).split("_")[0], \
                                "change_to":change_to, \
                                })
                else:
                    continue
            except:
                data.append({"changescore":"没有", \
                            "task":task, \
                            "old_score":"没有", \
                            "student_num":str(s).split("_")[1], \
                            "student":str(s).split("_")[0], \
                            "change_to":0, \
                            })
        newformset = formset_factory(CScore,extra=0)
        context={}
        context['task'] = task# if had input
        #context['students'] = students
        #context['scores'] = scores
        context['formset']  = newformset(initial = data)
        return render(request,'teacher/changescore.html',context)
    else:
        task = get_object_or_404(TeachingTask,id = taskpk)
        students = Student.objects.filter(classes = task.classes)
        scores = Score.objects.filter(task = task)
        #changes = Change_Score
        newformset = formset_factory(CScore,extra=0)
        #构建data=[{},{}]和formset数据进行比较对变化的数据进行更新
        data = []
        for s in students:
            try:
                score = Score.objects.get(task=task,student=s)
                try:
                    change_to = Change_Score.objects.get(changescore=score).change_to
                except:
                    change_to = 0
                data.append({"changescore":score.pk, \
                            "task":task, \
                            "old_score":score.score, \
                            "student_num":str(s).split("_")[1], \
                            "student":str(s).split("_")[0], \
                            "change_to":change_to, \
                            })
            except:
                data.append({"changescore":"没有", \
                            "task":task, \
                            "old_score":"没有", \
                            "student_num":str(s).split("_")[1], \
                            "student":str(s).split("_")[0], \
                            "change_to":0, \
                            })
        
        #使用表单自带的has_changed方法进行验证？
        f = newformset(request.POST)
        if f.is_valid():
            print(f)
            for i in f:
                the_changed = []#用于记录更改的信息
                score = Score.objects.get(pk = int(i.cleaned_data['changescore']))
                if int(i.cleaned_data['old_score']) != int(i.cleaned_data['change_to']) and \
                    score.is_changed == False:
                    change_to = Change_Score()
                    change_to.changescore = score
                    change_to.change_to = int(i.cleaned_data['change_to'])
                    change_to.save()
                    score.is_changed = True
                    score.save()
                else:
                    continue
            #返回教学任务选择界面
            return redirect('/teacher')
        else:
            context={}
            context['task'] = task
            context['formset']  = f
            return render(request,'teacher/changescore.html',context)
        
@login_required(login_url="/teacher/")
def teacher_attendance(request,taskpk):
    task = TeachingTask.objects.get(pk = taskpk)
    students = Student.objects.filter(classes = task.classes)
    #formset = AttendanceForm(classes = task.classes)
    attendance_set = Attendance.objects.filter(task = task)

    if request.method == "POST":
        students_pk = request.POST.getlist('student')
        taskpk = request.POST.get('taskpk',None)
        attendance_reason = request.POST.get('attendance_reason',None)
        attendance_reason = AttendanceReason.objects.get(name = attendance_reason )
        task = TeachingTask.objects.get(pk = taskpk )
        attendance_time = request.POST.get('attendance_time',None)
        for s in students_pk:
            a = Attendance()
            student = Student.objects.get(pk = int(s))
            a.student = student
            a.task = task
            a.attendance_time = attendance_time
            a.attendance_reason = attendance_reason
            try:
                a.save()
            except:
                return HttpResponse("已经存在")

    #传入任务班级
    formset = AttendanceForm(classes = task.classes)
    return render(request,'teacher/attendance.html',locals())

#from administrative.forms import SelectTeacherForm
from course.models import Course
from teachingtask.forms import TaskForm

@login_required(login_url="/teacher/")

def select_teacher(request):
    name = request.user.username
    user = User.objects.get(username = name)
    #teacher_info
    teacher = Teacher.objects.get(teacher = user)
    group_master = teacher.is_group_master
    #学年学期
    semester = Semester.objects.get(is_execute = True)
    newformset = formset_factory(TaskForm,extra=0)
    
    if request.method == "POST":
        formset = newformset(request.POST)
        #print(formset)
        if formset.is_valid():
            #print(formset)
            for aform in formset:
                task = aform.cleaned_data['task']
                teacher = aform.cleaned_data['teacher']
                print(task,"+++",teacher)
            return redirect('/teacher/select_teacher/')
        else:
            context = {}
            context['iscore'] = formset
            return render(request,'teacher/select_teacher.html',context)



    else:
        #得到所属教研室 teacher.belong_to
        #得到教师select
        #formset = SelectTeacherForm(development = teacher.belong_to)
        #得到课程这个课程为所有课程
        courses = Course.objects.filter(belong_to = teacher.belong_to)
        task = TeachingTask.objects.filter(semester = semester).order_by('course')
        #反向查询加快速度？？？？？？？？？？？？？？？
        
        #ttt = TeachingTask.objects.filter()
        data = []
        for t in task:
            if t.course in courses:
                data.append(
                    {
                        "task":t.pk,
                        "course":t.course,
                        "semester":t.semester,
                        "before_teacher":t.teacher,
                        "classes":t.classes
                    }
                )
        context = {}
        # context['tasks'] = tasks
        context['group_master'] = group_master
        context['iscore'] = newformset(initial = data)
        return render(request,'teacher/select_teacher.html',context)



def print_score(request,taskpk):
    task = TeachingTask.objects.get(pk = taskpk)

    scores = Score.objects.filter(task = task,root__isnull=True)
    #有多少条数据
    scores_num = scores.count()
    #构建数据
    #假设成绩单可以显示50条数据
    #计为25行数据 data 中存储25行数据
    data = []
    step = 0
    for i in range(scores_num):
        if step == 0:
            adata = []
            adata.append(scores[i])
            step += 1
            continue
        if step == 1:
            adata.append(scores[i])
            data.append(adata)
            adata = []
            step = 0
            continue

    if len(data[-1]) == 1 :
        data[-1].append("")
    
    if len(data)< 25:
        for i in range(len(data),25):
            data.append(["",""])




    context = {}
    context['task'] = task
    context['scores'] = data
    return render(request,'teacher/print_score.html',context)

