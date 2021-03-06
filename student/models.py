from django.db import models
# Create your models here.

from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from classes.models import Classes

class mystudentobjects(models.Manager):
    def get_queryset(self):
        return super(mystudentobjects,self).get_queryset().filter(student__is_active=True)


class Student(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE,related_name = "students")
    is_student = models.BooleanField(default = True)
    student_num = models.CharField(unique=True,max_length=20)
    classes = models.ForeignKey(Classes,on_delete=models.DO_NOTHING,null=True)
    nick_name = models.CharField(max_length=12,null=True,blank = True)
    objects = models.Manager()
    msobjects = mystudentobjects()

    def __str__(self):
        return self.student.username
    class Meta:
        ordering = ('classes','student_num')
        verbose_name = '学生'
        verbose_name_plural = '学生'