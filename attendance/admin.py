from django.contrib import admin
from .models import Attendance,AttendanceReason
# Register your models here.
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display=('task','student','create_time', \
        'attendance_time','attendance_reason','attendance_change', \
            'attendance_detail')


@admin.register(AttendanceReason)

class AttendanceReasonAdmin(admin.ModelAdmin):
    list_display=('name',)