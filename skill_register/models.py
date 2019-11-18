from django.db import models
from major.models import Major
from student.models import Student
from teachingtask.models import Semester
# Create your models here.

class SkillProject(models.Model):
    name = models.CharField(max_length=20,unique=True)
    photo = models.ImageField(upload_to='skillproject/%Y/%m/%d/',blank=True,null=True)
    context = models.CharField(max_length=200,blank=True,null=True)
    skilltype = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    is_sell = models.BooleanField(default=False)
    majors = models.ManyToManyField(Major)
    place = models.CharField(max_length=100,blank=True,null=True)
    game_time = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '技能大赛项目'
        verbose_name_plural = '技能大赛项目'
        ordering = ('create_time','is_sell',)

class SkillChoose(models.Model):
    skillproject = models.ForeignKey(SkillProject,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '技能大赛报名信息'
        verbose_name_plural = '技能大赛报名信息'
        #ordering = ('create_time','is_sell',)
