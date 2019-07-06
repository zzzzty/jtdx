from django.db import models

# Create your models here.
from teachingtask.models import Semester
from course.models import Course
from teacher.models import Teacher

class MakeUpTask(models.Model):
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING, \
        related_name="course_semester")
    execute_semester = models.ForeignKey(Semester,on_delete=models.DO_NOTHING, \
        related_name="makeup_execute_semester")
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    make_up = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s %s"%(self.course,self.semester,self.execute_semester,self.teacher)
    class Meta:
        unique_together = ['course','semester','execute_semester','teacher','make_up']
        ordering = ['create_time']
