import os 
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jtdx.settings')
django.setup()

import xlrd
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

basename =os.path.dirname(os.path.abspath(__file__)) 
tablename = os.path.join(basename,"makeup.xlsx")


table = xlrd.open_workbook(tablename)
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

from make_up.models import MakeUpTask
from teachingtask.models import Semester
from teacher.models import Teacher
from student.models import Student
from course.models import Course

for i in range(1,nrows):
    #班级
    print("第%s"%i,end="||||")
    course = get_value(data,i,4)
    year = get_value(data,i,5)
    period = get_value(data,i,6)
    teacher = get_value(data,i,2)
    student_num = get_value(data,i,0)
    student_name = get_value(data,i,1) 
    student_ = student_name+"_"+student_num
    
    make_up = 3
    is_input = False

    semester = Semester.objects.get(semester_year=year,semester_period=period)
    execute_semester = Semester.objects.get(is_execute=True)
    teacher = Teacher.objects.get(teacher__username = teacher)
    student = Student.objects.get(student__username=student_)
    course = Course.objects.get(name = course)
    try:
        newmakeup = MakeUpTask.objects.get(semester=semester,execute_semester=execute_semester, \
            make_up=make_up,student=student,course=course)
        print("have it")
        newmakeup.teacher = teacher
        newmakeup.make_up = make_up
        newmakeup.save()
    except:
        newmakeup = MakeUpTask()
        newmakeup.semester=semester
        newmakeup.execute_semester = execute_semester
        newmakeup.teacher = teacher
        newmakeup.student = student
        newmakeup.make_up = make_up
        newmakeup.course = course
        newmakeup.is_input = is_input
        newmakeup.save()
        print("save it")