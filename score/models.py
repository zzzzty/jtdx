from django.db import models
from teachingtask.models import TeachingTask 
from student.models import Student
from teacher.models import Teacher
# Create your models here.

#使用content_type 重写应该

class Score(models.Model):
    task =  models.ForeignKey(TeachingTask,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    is_changed = models.BooleanField(default=False)
    score_input_teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING, \
        related_name="score_input_teachers",null=True)
    #使用树结构记录学生补考成绩等信息
    root = models.ForeignKey('self',null=True,related_name='rootscore', \
        on_delete=models.CASCADE,blank=True)

    make_up = models.IntegerField(default=1)
    make_up_teacher = models.ForeignKey(Teacher,related_name="make_up_teacher" \
        ,on_delete=models.DO_NOTHING,null=True)
    is_make_up_input = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s"%(self.task,self.student,str(self.score))
    class Meta:
        unique_together = ['task','student','make_up','root']
        ordering = ['task__semester_year','task__semester_period','student__student_num']

class Change_Score(models.Model):
    changescore = models.ForeignKey(Score,on_delete=models.DO_NOTHING)
    #控制是否允许更改
    is_pass_order = models.BooleanField(default=False)
    change_to = models.IntegerField(default=0)
    def __str__(self):
        return "%s %s"%(self.changescore,self.change_to)