from django.db import models

from teacher.models import Teacher
# Create your models here.


class TeacherBaseWork(models.Model):
    name = models.CharField(max_length = 10)
    teacher = models.ForeignKey(Teacher,on_delete = models.DO_NOTHING)
    weights = models.FloatField()

    def __str__(self):
        return "%s %s %s"%(self.teacher,self.name,self.weights) 

    class Meta:
        ordering = ['teacher','name']
        unique_together=('teacher','name')