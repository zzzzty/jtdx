from django.contrib import admin
from .models import Tevaluation,Evalution_score,Comment
# Register your models here.

@admin.register(Tevaluation)
class TevaluationAdmin(admin.ModelAdmin):
    list_display=('name','weights')
    search_fields=('id','name')


@admin.register(Evalution_score)
class Evalution_scoreAdmin(admin.ModelAdmin):
    list_display=('evalution','student','teacher','semester','score','course')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('teacher','student','text','comment_time')