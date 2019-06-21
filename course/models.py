
from django.db import models
from teacher.models import Teacher
from administrative.models import TeacherDevelopment
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length = 20,unique=True)
    #create teacher
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    belong_to = models.ForeignKey(TeacherDevelopment,on_delete=models.DO_NOTHING,null = True)
    #所属教研室
    #创建时间
    #创建人
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'