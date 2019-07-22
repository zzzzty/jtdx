from django.contrib import admin
from .models import MakeUpTask
# Register your models here.
@admin.register(MakeUpTask)
class MakeUpTaskAdmin(admin.ModelAdmin):
    list_display=('course','semester','execute_semester','teacher','student','make_up','is_input')
