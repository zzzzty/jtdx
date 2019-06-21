from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.student_home,name="student_home"),
    #path('teacher_register/',views.register,name="teacher_register"),
]