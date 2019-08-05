from django.db import models

# Create your models here.
class DocFile(models.Model):
    name = models.CharField(max_length = 20,verbose_name = "名称")
    content = models.CharField(max_length = 20,verbose_name="简介")
    filepath = models.FileField(upload_to='files/%Y/%m/%d/',blank=True,null=True,verbose_name="下载")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = "创建时间")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = '文件上传'
        ordering = ('-create_time',)
