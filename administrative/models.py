from django.db import models

# Create your models here.

class Administrative(models.Model):
    name = models.CharField(max_length = 20,verbose_name="专业科名称")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '专业科名称'
        verbose_name_plural = '专业科名称'


class TeacherDevelopment(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    administrative = models.ForeignKey(Administrative,on_delete=models.DO_NOTHING)
    def __str__(self):
        return "%s %s"%(self.administrative.name,self.name)


