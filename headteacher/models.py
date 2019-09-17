from django.db import models

# Create your models here.
from teachingtask.models import Semester
from classes.models import Classes
from teacher.models import Teacher


class HeadTeacher(models.Model):
    classes = models.ForeignKey(Classes,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,null=True)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING,null=True)
    class Meta:
        verbose_name = "班主任"
        verbose_name_plural = "班主任"