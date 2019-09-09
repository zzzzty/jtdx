from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.student_home,name="student_home"),
    #path('teacher_register/',views.register,name="teacher_register"),
    path('rate_teacher/',views.rate_teacher,name="rate_teacher"),
    path('mycourse/',views.my_course,name="my_course"),
]