from django.contrib import admin
from .models import Classes
# Register your models here.
@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display=['name','major','teacher']