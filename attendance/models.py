from django.db import models
from teachingtask.models import TeachingTask
from student.models import Student
# Create your models here.

class AttendanceReason(models.Model):
    name = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name





class Attendance(models.Model):
    task =  models.ForeignKey(TeachingTask,on_delete = models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete = models.DO_NOTHING)
    #考勤创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    #考勤的时间
    attendance_time = models.DateField()
    #被考勤的原因
    attendance_reason = models.ForeignKey(AttendanceReason,on_delete=models.DO_NOTHING)
    #考勤更改为
    attendance_change =  models.ForeignKey(AttendanceReason,on_delete=models.DO_NOTHING, \
                        blank=True,null=True,related_name="attendance_change")

    class Meta:
         unique_together = ['task','student','attendance_time']

