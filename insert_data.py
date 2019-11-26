import os 
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jtdx.settings')
django.setup()

import xlrd
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

#table = xlrd.open_workbook('/home/liu/project/django_web/jtdx/chengji.xls')

basename =os.path.dirname(os.path.abspath(__file__)) 
dirtable = os.path.join(basename,"chengji.xlsx")
table = xlrd.open_workbook(dirtable)

data = table.sheets()[0]
nrows = data.nrows
ncols = data.ncols

print(nrows,ncols)

def get_value(data,row_index,col_index):
    the_value = data.cell(row_index,col_index).ctype
    if the_value == 2:
        the_value = str(int(data.cell(row_index,col_index).value))
    else:
        the_value = str(data.cell(row_index,col_index).value)
    return the_value




from teacher.models import Teacher
theuser = Teacher.objects.filter(teacher__username='liu')[0]

for i in range(1,nrows):
    #学生姓名
    student = data.cell(i,1).value
    studentnickname = data.cell(i,1).value
    #学生学号
    student_num = get_value(data,i,0)
    #年级
    grade = get_value(data,i,14)
    #班级
    classes = get_value(data,i,15)
    #专业
    major = get_value(data,i,24)
    #学年学期
    semester_year = get_value(data,i,10)
    semester_period = get_value(data,i,11)
    #课程
    course = get_value(data,i,3)
    #教师
    teacher = get_value(data,i,12)
    
    if len(teacher)<1:
        teacher = "liu"
    #分数
    score = int(get_value(data,i,5))
    try:
        bukaoscore = int(get_value(data,i,6))
    except:
        bukaoscore = ""

    #chongxiuscore = int(get_value(data,i,7))


    from grade.models import Grade
    try:
        grade = Grade.objects.get(name = grade)
        #print(grade)
    except:
        newgrade = Grade()
        newgrade.name = grade
        newgrade.save()
        grade = newgrade
        print("nothavegrade")
    
    from major.models import Major
    try:
        #如果出现重复信息如何
        major = Major.objects.get(name = major,grade=grade)
    except:
        newmajor = Major()
        newmajor.name = major
        newmajor.grade = grade
        newmajor.save()
        major = newmajor
    from classes.models import Classes
    try:
        classes = Classes.objects.get(name = classes)
    except:
        newclasses = Classes()
        newclasses.name = classes
        newclasses.major = major
        newclasses.teacher = theuser
        newclasses.save()
        classes = newclasses

    from student.models import Student
    try:
        student = User.objects.get(username = student+"_"+student_num )
        try:
            student = Student.objects.get(student = student)
        except:
            newstudent = Student()
            newstudent.student_num = student_num
            newstudent.student = student
            newstudent.classes = classes
            newstudent.save()
            student = newstudent
    except:
        a = User.objects.create_user(student+"_"+student_num,"test@jtdx.com",student_num)
        newstudent = Student()
        newstudent.student_num = student_num
        newstudent.student = a
        newstudent.classes = classes
        newstudent.nick_name = studentnickname
        newstudent.save()
        student = newstudent

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
        newstudent = Student()
        newteacher = Teacher()
        newteacher.teacher = a
        newteacher.is_teacher = True
        newteacher.save()
        teacher = newteacher

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
            #teacher = teacher,
            course = course,
            classes = classes,
            semester = semester
            )
        #print("++++got one task")
    except:
        newteachingtask = TeachingTask()
        newteachingtask.teacher = teacher
        newteachingtask.course = course
        newteachingtask.classes = classes
        newteachingtask.semester = semester
        newteachingtask.is_input = True
        newteachingtask.save()
        teachingtask = newteachingtask
        #print("----save one task ")

    from score.models import Score

    try:
        score = Score.objects.get( \
            task = teachingtask,
            student = student,
            score = score
            )
    except:
        newscore = Score()
        newscore.task = teachingtask
        newscore.student = student
        newscore.score = score
        newscore.save()
        score = newscore
        #print("savesocre",str(i))

'''
#补考成绩录入
    if len(str(bukaoscore)) > 0 and score.score < 60:
        score = Score.objects.filter( \
        task = teachingtask,
        student = student
        )[0]
        try:
            bukaoscore = Score.objects.get( \
                task = teachingtask,
                student = student,
                score = int(bukaoscore),
                root = score
                )
        except:
            newscore = Score()
            newscore.task = teachingtask
            newscore.student = student
            newscore.score = bukaoscore
            newscore.root = score
            newscore.save()
            bukaoscore = newscore
            print("添加补考",str(i))
#    print(student,student_num,grade,classes,major)
'''
