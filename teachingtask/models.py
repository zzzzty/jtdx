
from django.db import models
from teacher.models import Teacher
from course.models import Course
from classes.models import Classes
# Create your models here.


class Semester(models.Model):
    semester_year = models.CharField(max_length = 20)
    semester_period = models.CharField(max_length = 5)
    #create_time = models.DateTimeField(auto_now_add=True)
    #当前学年是否为在执行
    is_execute = models.BooleanField(default=False)
    #学年开始时间及结束时间
    start_time = models.DateField(null=True)
    end_time = models.DateField(null=True)

    #上一学期
    root_semester = models.ForeignKey('self',null=True, \
        related_name='root_semesters', \
        on_delete=models.CASCADE,blank=True)
    #下一学期
    child_semester = models.ForeignKey('self',null=True, \
        related_name='child_semesters', \
        on_delete=models.CASCADE,blank=True)
    
    def __str__(self):
        return "%s学年 %s学期"%(self.semester_year,self.semester_period) 
    class Meta:
        ordering = ('semester_year','semester_period')

class TeachingTask(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,null=True)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    classes = models.ForeignKey(Classes,on_delete=models.DO_NOTHING)
    #学年学期
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_input = models.BooleanField(default=False)
    is_changed = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s %s %s"%(self.semester,self.course,self.classes) 
    class Meta:
        unique_together = ['semester','course','classes']
        verbose_name = '教学任务'
        verbose_name_plural = '教学任务'
        ordering = ('teacher__teacher__username',)