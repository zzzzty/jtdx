from django.db import models
from major.models import Major
from teacher.models import Teacher
# Create your models here.


class Classes(models.Model):
    name = models.CharField(max_length = 20)
    major = models.ForeignKey(Major,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'