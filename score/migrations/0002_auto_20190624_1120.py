# Generated by Django 2.2.2 on 2019-06-24 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ['task__semester_year', 'task__semester_period', 'student__student_num']},
        ),
    ]
