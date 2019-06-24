from django.contrib import admin
from .models import Score,Change_Score
# Register your models here.
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display=('task','student','score','make_up','make_up_teacher', \
        'is_make_up_input','is_changed','root')
    search_fields = ['student__student_num','task__course__name','task__classes__name',]


@admin.register(Change_Score)
class Change_ScoreAdmin(admin.ModelAdmin):
    list_display=('changescore','is_pass_order','change_to')

