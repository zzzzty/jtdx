
from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('id','name')
# Register your models here.
