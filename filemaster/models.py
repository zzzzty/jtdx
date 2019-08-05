from django.db import models

# Create your models here.
class DocFile(models.Model):
    name = models.CharField(max_length = 20)
    content = models.CharField(max_length = 20)
    filepath = models.FileField(upload_to='files/%Y/%m/%d/',blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = '文件上传'
        ordering = ('-create_time',)
