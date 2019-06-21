from django.db import models
from grade.models import Grade
import django.utils.timezone as timezone
# Create your models here.

class Major(models.Model):
    name = models.CharField('专业名称',max_length=20)
    grade = models.ForeignKey(Grade,on_delete=models.DO_NOTHING,verbose_name='年级')
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_updated_time = models.DateTimeField('最后更新时间',default = timezone.now)
    def __str__(self):
        return "%s级 %s"%(self.grade.name,self.name)
    class Meta:
        verbose_name = '专业'
        verbose_name_plural = '专业'