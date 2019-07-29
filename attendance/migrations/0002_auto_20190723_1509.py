# Generated by Django 2.2.2 on 2019-07-23 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0007_remove_teachingtask_level'),
        ('student', '0002_student_nick_name'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='attendance_detail',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('task', 'student', 'attendance_time', 'attendance_detail')},
        ),
    ]