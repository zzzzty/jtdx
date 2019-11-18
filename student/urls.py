from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('',views.student_home,name="student_home"),
    #path('teacher_register/',views.register,name="teacher_register"),
    path('rate_teacher/<int:teacherpk>/<int:coursepk>',views.rate_teacher,name="rate_teacher"),
    path('mycourse/',views.my_course,name="my_course"),
    path('myscores/',views.my_scores,name="my_scores"),
    path('myteacher/',views.my_teacher_list,name="my_teacher"),
    path('insert_evaluation/',views.insert_evaluation,name="insert_evaluation"),
    path('skillregister/',views.skillregister,name="skillregister"),
]