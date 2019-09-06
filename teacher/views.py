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
from django.http import JsonResponse
from django.db.models.aggregates import Count
from course.models import Course
from make_up.models import MakeUpTask
# Create your views here.
#教师登陆主页
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
                #print("___________",name)
                user = User.objects.get(username = name)#如果是个学生如何
                teacher = Teacher.objects.get(teacher = user)
                teachingtasks = TeachingTask.objects.filter(teacher=teacher)
                context = {}
                context['group_master'] = teacher.is_group_master
                context['name'] = name
                context['teachingtasks'] = teachingtasks
                return render(request,'teacher/teacher_task.html',context)
            except:
                context = {}
                context['teacherloginform'] = StudentLoginForm()
                return render(request,'student/student_home.html',context)
#注册
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
#教师教学任务
@login_required(login_url="/teacher/")
def teacher_task(request):
    #正常的教学任务
    name = request.user.username
    user = User.objects.get(username = name)
    #如果是个学生如何 使用try 方法解决
    teacher = Teacher.objects.get(teacher = user)
    #得到当前学年学期
    semester = Semester.objects.get(is_execute = True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    teachingtasks = TeachingTask.objects.filter(teacher=teacher,semester=semester)
    context = {}
    context['group_master'] = teacher.is_group_master
    #判断该教师是否为班主任
    classesmaster = Classes.objects.filter(teacher = teacher).count()
    context['classesmaster'] = classesmaster
    context['name'] = name
    context['teachingtasks'] = teachingtasks
    #重修的教学任务
    #需要更多的条件,execute_semester=semester
    scores = MakeUpTask.objects.filter(teacher=teacher, \
        execute_semester=semester,is_input = False) \
        .values_list('course','semester','make_up')
    #print(scores)
    final_coures ={}
    #任务标记是补考，重修还是其它
    makeupsign = []
    for s in scores:
        if s not in final_coures.keys():
            final_coures[s] = [1,]
        else:
            final_coures[s][0] += 1
        if s[2] not in makeupsign:
            makeupsign.append(s[2])
   # print(makeupsign)
    
    for s in final_coures.keys():
        #print(s[0])
        #print(s[1],"___")
        course = Course.objects.get(pk=s[0])
        semester = Semester.objects.get(pk=s[1])
        final_coures[s].append(course)
        final_coures[s].append(semester)
    #print(final_coures)
    if 2 in makeupsign:
        bukao = True
    else:
        bukao = False
    if 3 in makeupsign:
        chongxiu = True
    else:
        chongxiu = False
    if 4 in makeupsign:
        biyeqian = True
    else:
        biyeqian = False
    context['bukao'] = bukao
    context['chongxiu'] = chongxiu
    context['biyeqian'] = biyeqian
    context['scores'] = final_coures
    #print(final_coures)
    return render(request,'teacher/teacher_task.html',context)

from score.forms import IScore
from student.models import Student
from django.forms import formset_factory

#成绩录入
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
            context['iscore'] = newformset(initial = data)
            return render(request,'teacher/teacher_task.html',context)
            #return render(request,'teacher/teacher_score.html',context)
        else:
            context['iscore'] = f
            return render(request,'teacher/teacher_score.html',context)

from classes.models import Classes
@login_required(login_url="/teacher/")
#平时成绩单打印
def print_name(request,taskpk,sign):
    context = {}
    #sign 为1时返回班级名单
    if sign != 1:
        task = get_object_or_404(TeachingTask,id = taskpk)
        students = Student.objects.filter(classes = task.classes).order_by('classes','student_num')
        context['task'] =task
    else:
        classes = get_object_or_404(Classes,id = taskpk)
        students = Student.objects.filter(classes = classes)
        context['task'] = classes
    studentinfos = []
    for s in students:
        studentinfos.append(str(s.student.username).split("_"))
    context['students'] = studentinfos
    #next_loop = 45 - students.count()
    next_index = []
    for i in range(students.count()+1,45,1):
        next_index.append(i)
    context['next_index'] = next_index
    return render(request,'teacher/name.html',context)

#更改成绩请求
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
            #print(f)
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
#考勤
def teacher_attendance(request,taskpk):
    task = TeachingTask.objects.get(pk = taskpk)
    students = Student.objects.filter(classes = task.classes)
    #formset = AttendanceForm(classes = task.classes)
    attendance_set = Attendance.objects.filter(task = task).order_by('-create_time')
    #对教师是否有这个教学任务进行验证
    name = request.user.username
    user = User.objects.get(username = name)
    #teacher_info
    teacher = Teacher.objects.get(teacher = user)
    
    if task.teacher == teacher:
        if request.method == "POST":
            students_pk = request.POST.getlist('student')
            taskpk = request.POST.get('taskpk',None)
            attendance_reason = request.POST.get('attendance_reason',None)
            attendance_reason = AttendanceReason.objects.get(name = attendance_reason )
            task = TeachingTask.objects.get(pk = taskpk )
            attendance_time = request.POST.get('attendance_time',None)
            select_detail = request.POST.get('select_detail',None)
            for s in students_pk:
                a = Attendance()
                student = Student.objects.get(pk = int(s))
                a.student = student
                a.task = task
                a.attendance_time = attendance_time
                a.attendance_reason = attendance_reason
                a.attendance_detail = select_detail
                try:
                    a.save()
                except:
                    pass
                    #return HttpResponse("已经存在")

        #传入任务班级
        formset = AttendanceForm(classes = task.classes)
        return render(request,'teacher/attendance.html',locals())
    else:
        return HttpResponse('没有这个教学任务')

#from administrative.forms import SelectTeacherForm
from course.models import Course
from teachingtask.forms import TaskForm,TaskmodelForm,Select_Teacher

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
                aselect = aform.cleaned_data['aselect']
                #task 为教学任务的主键值,teacher为所属教研组,aselect最新选择的教师
                #print(task,"+++",teacher,"+++",aselect)
                oldtask = TeachingTask.objects.get(pk=task)
                newteacher = get_object_or_404(Teacher,teacher__username=aselect)
                if newteacher != oldtask.teacher:
                    #print(oldtask.teacher,newteacher)
                    oldtask.teacher = newteacher
                    oldtask.is_changed = True
                    oldtask.save()

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
        task = TeachingTask.objects.filter(semester = semester,is_changed=False).order_by('course')
        #反向查询加快速度？？？？？？？？？？？？？？？
        #ttt = TeachingTask.objects.filter()
        development_teachers = Teacher.objects. \
            filter(belong_to = teacher.belong_to).values_list('pk','teacher__username')

        #print("heheh",(development_teachers))

        data = []
        for t in task:
            if t.course in courses:
                data.append(
                    {
                        "task":t.pk,
                        "course":t.course,
                        "semester":t.semester,
                        "before_teacher":t.teacher,
                        "classes":t.classes,
                    }
                )
        context = {}
        # context['tasks'] = tasks
        #print(task.count)
        context['group_master'] = group_master
        #newformset = newformset(form_kwargs={'belong':teacher.belong_to})
        context['iscore'] = newformset(initial = data)
        context['belong'] = teacher.belong_to.pk
        return render(request,'teacher/select_teacher.html',context)

@login_required(login_url="/teacher/")
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
    #有bug 单数的信息不会显示
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
    #解决单数不显示的问题
    if scores_num%2 == 1:
        data.append(adata)

    if len(data)>0:
        if len(data[-1]) == 1 :
            data[-1].append("")
    
    if len(data)< 30:
        for i in range(len(data),30):
            data.append(["",""])

    context = {}
    context['task'] = task
    context['scores'] = data
    context['scores_num'] = scores_num
    return render(request,'teacher/print_score.html',context)

def group_teacher(request):
    belong = request.GET.get('belong',None)
    if belong:
        teachers = Teacher.objects.filter(belong_to_id=belong).order_by('-is_group_master','teacher__username')
        #teachers = Teacher.objects.filter()
        list_data = []
        for t in teachers:
            list_data.append([str(t.pk),str(t.teacher)])
        data = {}
        data['teachers'] = list_data
        #print(data)
        return  JsonResponse(data)


@login_required(login_url="/teacher/")
def input_score(request,coursepk,semesterpk,make):
    #构建新的make_up应用，对重修、补考进行统一的管理？？
    #如果是个学生如何 使用try 方法解决
    #make为int 是哪种考试类型 是补考 还是重修
    name = request.user.username
    user = User.objects.get(username = name)
    teacher = Teacher.objects.get(teacher = user)
    course = get_object_or_404(Course,pk=coursepk)
    semester = get_object_or_404(Semester,pk=semesterpk)
    make_up = make
    data = input_score_formsetdata(course=course,semester=semester, \
        execute_semester=semester,teacher=teacher,make=make)
    context = {}
    context['task'] = course
    #context['taskpk'] = taskpk
    if make_up == 2:
        context['classes'] = "补考"+str(semester)
    if make_up == 3:
        context['classes'] = "重修"+str(semester)

    if request.method == "POST":
        newformset = formset_factory(IScore,extra=0)
        f = newformset(request.POST,request.FILES)
        #print(f.as_table())
        if f.is_valid():
            for i in f:
                #student_username字段隐藏的是分数id
                scorepk = i.cleaned_data['student_username']
                score = i.cleaned_data['score']
                #int 2 是重修
                task = i.cleaned_data['task']
                #print(scorepk,score,task,teacher)
                basescore = Score.objects.filter(pk = scorepk)[0]
                try:
                    basescore = Score.objects.get(root = basescore,make_up=make_up)
                    print("now we have it%s"%basescore)
                except:
                    if score != 0:
                        makescore = Score()
                        makescore.task = basescore.task
                        makescore.student = basescore.student
                        makescore.score = score
                        makescore.score_input_teacher = teacher
                        makescore.root = basescore
                        makescore.make_up = make_up
                        makescore.execute_semester = get_object_or_404(Semester,pk=semesterpk)
                        makescore.is_make_up_input = True
                        makescore.save()
                        mtask = MakeUpTask.objects.get(course=course,semester = semester, \
                                        execute_semester = semester,teacher = teacher, \
                                        make_up=make_up,is_input=False,student = basescore.student)
                        mtask.is_input = True
                        mtask.save()
                    else:
                        pass
            data = input_score_formsetdata(course=course,semester=semester \
                ,execute_semester=semester,teacher=teacher,make=make)
            f = newformset(initial = data)
            context['iscore'] = f
        else:
            context['iscore'] = f
    else:
        newformset = formset_factory(IScore,extra=0)
        context['iscore']  = newformset(initial = data)
    return render(request,'teacher/teacher_makeup_score.html',context)

def input_score_formsetdata(course,semester,execute_semester,teacher,make):
    data = []
     #进行查询那些成绩是需要录入的,以下查询限定了某学期的某中课程
    tasks = MakeUpTask.objects.filter(course=course,semester = semester, \
                execute_semester = semester,teacher = teacher, \
                make_up=make,is_input=False).order_by('student__classes','-student__student_num')
    for s in tasks:
        hiddenelement = Score.objects.get(student = s.student,task__course=s.course, \
            task__semester=s.semester,make_up = 1)
        data.append({'student_username':hiddenelement.pk, \
                    'student_num':s.student.student_num, \
                    'student':str(s.student).split('_')[0], \
                    'task':2, \
                    'score':0
                    })
    return data

@login_required(login_url="/teacher/")
def print_name_makeup(request,coursepk,semesterpk,make):
    #coursepk 课程id
    #semesterpk 课程所属学期
    #execute_semester 课程执行学期
    #students = Student.objects.filter(classes = task.classes)
    
    course = get_object_or_404(Course,id=coursepk)
    semester = get_object_or_404(Semester,id=semesterpk)
    execute_semester = Semester.objects.get(is_execute=True)
    #teacher_info
    name = request.user.username
    user = User.objects.get(username = name)
    teacher = Teacher.objects.get(teacher = user)
    
    makeuptasks = MakeUpTask.objects.filter(course=course,semester=semester, \
                teacher = teacher,is_input=False).order_by('student__student_num')
    
    
    studentinfos = []
    for s in makeuptasks:
        studentinfos.append(str(s.student.student.username).split("_"))
    context = {}
    context['students'] = studentinfos
    context['task'] =str(course)+str(semester)
    #next_loop = 45 - students.count()
    next_index = []
    for i in range(makeuptasks.count()+1,45,1):
        next_index.append(i)
    context['next_index'] = next_index
   
    return render(request,'teacher/name.html',context)
@login_required(login_url="/teacher/")
def myclasses(request):
    
    name = request.user.username
    user = User.objects.get(username = name)
    teacher = Teacher.objects.get(teacher = user)
    #历史的班主任信息如何处理
    classes = Classes.objects.filter(teacher = teacher)
    students = Student.objects.filter(classes = classes[0])
    context = {}
    context['classes']= classes
    classesmaster = Classes.objects.filter(teacher = teacher).count()
    context['classesmaster'] = classesmaster
    context['students']=students

    return render(request,'teacher/myclasses.html',context)

@login_required(login_url="/teacher/")
def teacher_query_score(request,classespk):
    #使用用户模型的中的isactive进行用户是否有效进行判断
    students = Student.objects.filter(classes_id = classespk,student__is_active = True).order_by('student_num')
    return render(request,'namelist.html',{'students':students})

from django.db.models import Max,Avg
@login_required(login_url="/teacher/")
def student_score(request,studentpk):
    #所有该生成绩
    #students = Score.objects.filter(student_id=studentpk).order_by('task__semester','-task__course')
    scores = Score.objects.filter(student_id=studentpk).order_by('task__semester','-task__course'). \
        values_list('task','student').annotate(Max("score"))#task_id,student_id,socre这个是一个list
    #如果有重修等取最大成绩
    data = []
    for s in scores:
        #task_id,student_id,socre这个是一个list
        score = Score.objects.get(task_id= s[0],score=s[2],student_id=s[1])
        #print(data)
        data.append(score)
    return render(request,'score_list.html',{'students':data,'scores':scores})
    #return render(request,'score_list.html',{'students':students,'scores':scores})

@login_required(login_url="/teacher/")
def print_class_student_scores(request,classpk):
    #得到班级信息
    classes = get_object_or_404(Classes,pk = classpk)
    #得到学生信息
    students = Student.objects.filter(classes = classes,student__is_active = True). \
        order_by('student_num')
    #构建成绩报表
    class_score_dict = {}


    for student in students:
        if student not in class_score_dict:
            class_score_dict[student] = {}
        #task_id,student_id,socre这个是一个list[(),(),()]
        a_student_scores = Score.objects.filter(student=student).order_by('task__semester', \
            '-task__course').values_list('task','id').annotate(Max("score"))
        for ascore in a_student_scores:
            taskpk = ascore[0]#max
            task = TeachingTask.objects.get(pk = taskpk)
            semester = task.semester
            score = Score.objects.get(pk=ascore[1])
            if semester not in class_score_dict[student]:
                class_score_dict[student][semester] = {}
                class_score_dict[student][semester]["count"] = 1
                class_score_dict[student][semester]["detail"] = [score]
            else:
                class_score_dict[student][semester]["count"] += 1
                class_score_dict[student][semester]["detail"].append(score)
            #if taskpk not in class_score_dict[student]:
            #    class_score_dict[student][taskpk] = {}
    for student in class_score_dict:
        print(student)
        for semester in class_score_dict[student]:
            detaillen =len(class_score_dict[student][semester]['detail'])
            if detaillen<12:
                for k in range(detaillen,12):
                   class_score_dict[student][semester]['detail'].append("")

    return render(request,'print_scores_list.html',locals())

from filemaster.models import DocFile
from filemaster.tables import DocFileTable
from django_tables2 import RequestConfig
def filemaster(request):
    table = DocFileTable(DocFile.objects.all())
    context = {}
    RequestConfig(request).configure(table)
    context['files'] = table
    return render(request,'teacher/filemaster.html',context)
    

