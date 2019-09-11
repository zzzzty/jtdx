from django.db import models
from student.models import Student
from teacher.models import Teacher
from teachingtask.models import Semester
from course.models import Course
# Create your models here.
class Tevaluation(models.Model):
    name = models.CharField('名称',max_length=20)
    content = models.CharField('简介',max_length=20)
    def __str__(self):
        return self.name

class Evalution_score(models.Model):
    evalution = models.ForeignKey(Tevaluation,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True)
    score = models.IntegerField(default=1)
    class Meta:
        unique_together = ['evalution','student','teacher','semester','course']
