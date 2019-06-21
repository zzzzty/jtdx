from django.contrib import admin
from .models import Administrative,TeacherDevelopment
# Register your models here.
@admin.register(Administrative)
class AdministrativeAdmin(admin.ModelAdmin):
    list_display=('name','create_time')
    search_fields = ['name',]

@admin.register(TeacherDevelopment)
class TeacherDevelopmentAdmin(admin.ModelAdmin):
    list_display = ('name','administrative')