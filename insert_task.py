import os 
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jtdx.settings')
django.setup()

import xlrd
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

table = xlrd.open_workbook('/home/liu/project/django_web/jtdx/2019-2020-1.xls')
data = table.sheets()[0]
nrows = data.nrows
ncols = data.ncols


def get_value(data,row_index,col_index):
    the_value = data.cell(row_index,col_index).ctype
    if the_value == 2:
        the_value = str(int(data.cell(row_index,col_index).value))
    else:
        the_value = str(data.cell(row_index,col_index).value)
    return the_value

from teacher.models import Teacher
theuser = Teacher.objects.all()[0]

for i in range(1,nrows):
    #班级
    classes = get_value(data,i,4)
    #学年学期
    semester_year = get_value(data,i,1)
    semester_period = get_value(data,i,2)
    #课程
    course = get_value(data,i,0)
    #教师
    teacher = get_value(data,i,9)
    #print(classes,semester_year,semester_period,course,teacher)
    grade = get_value(data,i,10)
    if len(teacher)<1:
        teacher = "liu"
    #分数

    from grade.models import Grade
    try:
        grade = Grade.objects.get(name = grade)
        #print(grade)
    except:
        newgrade = Grade()
        newgrade.name = grade
        newgrade.save()
        print("we have save a new grade %r"%newgrade)
        grade = newgrade

    from classes.models import Classes
    try:
        classes = Classes.objects.get(name = classes)
    except:
        print("+++++++++++------we dont find this %r"%classes,end="||")
        newclass = Classes()
        newclass.name = classes
        newclass.save()
        #continue
        classes = newclass
    #teacher
    try:
        teacher = User.objects.get(username = teacher )
        try:
            teacher = Teacher.objects.get(teacher = teacher)
        except:
            newteacher = Teacher()
            newteacher.teacher = teacher
            newteacher.save()
            teacher = newteacher
    except:
        a = User.objects.create_user(teacher,"teacher@jtdx.com","jtdxjwk")
        newteacher = Teacher()
        newteacher.teacher = a
        newteacher.is_teacher = True
        newteacher.save()
        teacher = newteacher
        print("we have save a new user %r"%teacher,end="||")

    from course.models import Course 
    try:
        course = Course.objects.get(name = course)
    except:
        newcourse = Course()
        newcourse.name = course
        newcourse.teacher = theuser
        newcourse.save()
        course = newcourse

    from teachingtask.models import TeachingTask,Semester
    try:
        semester = Semester.objects.get(semester_year= semester_year,semester_period = semester_period)
    except:
        newsemester = Semester()
        newsemester.semester_year = semester_year
        newsemester.semester_period = semester_period
        newsemester.save()
        semester = newsemester
    
    try:
        teachingtask = TeachingTask.objects.get( \
            course = course,
            classes = classes,
            semester = semester
            )
    except:
        newteachingtask = TeachingTask()
        newteachingtask.teacher = teacher
        newteachingtask.course = course
        newteachingtask.classes = classes
        newteachingtask.semester = semester
        newteachingtask.is_input = False
        newteachingtask.save()
        teachingtask = newteachingtask
        print("----save one task %r"%teachingtask)
