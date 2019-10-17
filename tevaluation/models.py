from django.db import models
from student.models import Student
from teacher.models import Teacher
from teachingtask.models import Semester
from course.models import Course
from django.contrib.auth.models import User
# Create your models here.
class Tevaluation(models.Model):
    name = models.CharField('名称',max_length=20)
    content = models.CharField('简介',max_length=200)
    weights = models.FloatField("权重",default=0)
    def __str__(self):
        return "测评项目：%s 权重：%s"%(self.name,self.weights)

class Evalution_score(models.Model):
    evalution = models.ForeignKey(Tevaluation,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True)
    score = models.IntegerField(default=1)
    class Meta:
        unique_together = ['evalution','student','teacher','semester','course']

class Comment(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    #course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    root = models.ForeignKey('self',null=True,related_name='root_comment',on_delete=models.DO_NOTHING)
    #回复给哪条信息的
    parent = models.ForeignKey('self',null=True,related_name='parent_comment',on_delete=models.DO_NOTHING)
    #此条回复是回复给谁的
    reply = models.ForeignKey(User,related_name='replies',null=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']