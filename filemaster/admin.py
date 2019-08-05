from django.contrib import admin

# Register your models here.
from .models import DocFile
# Register your models here.
@admin.register(DocFile)
class DocFileAdmin(admin.ModelAdmin):
    list_display=['name','create_time','content','filepath']