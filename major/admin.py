from django.contrib import admin
from .models import Major
# Register your models here.
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display=('name','pk','grade','create_time','last_updated_time')
    search_fields = ['name']
    ordering = ['create_time',]