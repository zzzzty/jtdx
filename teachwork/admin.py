from django.contrib import admin
from .models import TeacherBaseWork
# Register your models here.


@admin.register(TeacherBaseWork)
class TeacherBaseWorkAdmin(admin.ModelAdmin):
    list_display = ['name','teacher','weights']
    search_fields = ['name','teacher__teacher__username',]
