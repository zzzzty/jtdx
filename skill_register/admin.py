from django.contrib import admin

# Register your models here.
from .models import SkillProject,SkillChoose
@admin.register(SkillProject)
class SkillProjectAdmin(admin.ModelAdmin):
    list_display = ('name','skilltype','create_time',)

@admin.register(SkillChoose)
class SkillChooseAdmin(admin.ModelAdmin):
    list_display = ('skillproject','student','semester')