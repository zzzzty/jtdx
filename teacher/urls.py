from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.teacher_home,name="teacher_home"),
    path('teacher_register/',views.register,name="teacher_register"),
    path('teacher_task/',views.teacher_task,name='teacher_task'),
    path('teacher_score/',views.teacher_insert_score,name='teacher_score'),
    path('print_name/<int:taskpk>/<int:sign>',views.print_name,name = 'print_name'),
    path('change_score/<int:taskpk>',views.change_score,name='change_score'),
    path('attendance/<int:taskpk>',views.teacher_attendance,name = 'attendance'),
    path('select_teacher/',views.select_teacher,name="select_teacher"),
    path('print_score/<int:taskpk>',views.print_score,name = 'print_score'),
    path('groupteacher/',views.group_teacher,name='groupteacher'),
    path('input_score/<int:coursepk>/<int:semesterpk>/<int:make>',views.input_score,name="input_score"),
    path('print_name/<int:coursepk>/<int:semesterpk>/<int:make>',views.print_name_makeup,name = 'print_name_makeup'),
    path('myclasses/',views.myclasses,name='myclasses'),
    path('teacher_query_score/<int:classespk>',views.teacher_query_score,name='teacher_query_score'),
    path('teacher_query_score/student/<int:studentpk>',views.student_score,name='student_query_score'),
    path('filemaster/',views.filemaster,name="filemaster"),
    path('my_evalution/',views.my_evalution,name="my_evalution"),
   #path('refresh-captcha/',views.refresh_captcha,name="refresh-captcha"),
    path('printclassstudentscore/<int:classpk>',views.print_class_student_scores,name="printclassstudentscore"),
]