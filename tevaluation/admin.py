from django.contrib import admin
from .models import Tevaluation,Evalution_score
# Register your models here.

@admin.register(Tevaluation)
class TevaluationAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('id','name')


@admin.register(Evalution_score)
class Evalution_scoreAdmin(admin.ModelAdmin):
    list_display=('evalution','student','teacher','semester','score')