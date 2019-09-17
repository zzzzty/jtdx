from django.contrib import admin
from .models import HeadTeacher
# Register your models here.
@admin.register(HeadTeacher)
class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ['classes','semester','teacher']