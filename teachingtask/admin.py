from django.contrib import admin
from .models import TeachingTask,Semester
# Register your models here.


@admin.register(TeachingTask)
class TeachingTaskAdmin(admin.ModelAdmin):
    list_display = ['semester','teacher','course','classes','is_changed','create_time']
    search_fields = ['classes__name','teacher__teacher__username',]

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester_year','semester_period','is_execute',]
