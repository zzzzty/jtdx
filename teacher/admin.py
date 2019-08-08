from django.contrib import admin
from .models import Teacher
# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher','is_group_master','belong_to']
    search_fields = ['teacher__username',]

