from django.contrib.auth.models import User
from django.db import models
#年级
class Grade(models.Model):
    name = models.CharField('年级名称',max_length=10)
    def __str__(self):
        return self.name
    #只有verbose_name 显示 '年级s'
    class Meta:
        verbose_name = '年级'
        verbose_name_plural = '年级'
