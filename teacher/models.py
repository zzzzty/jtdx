from django.db import models
from django.contrib.auth.models import User
from administrative.models import TeacherDevelopment
# Create your models here.

class Teacher(models.Model):
    teacher = models.OneToOneField(User,on_delete=models.CASCADE,related_name = "teachers")
    is_group_master = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    belong_to = models.ForeignKey(TeacherDevelopment,on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return self.teacher.username
    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = '教师信息'
        ordering = ('belong_to','teacher__username',)