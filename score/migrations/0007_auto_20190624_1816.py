# Generated by Django 2.2.2 on 2019-06-24 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0007_remove_teachingtask_level'),
        ('student', '0002_student_nick_name'),
        ('score', '0006_score_root'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('task', 'student', 'make_up', 'root')},
        ),
    ]