from django.contrib import admin
from .models import Student
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student','student_num','classes','is_student']
    search_fields=('student__username','classes__name')
