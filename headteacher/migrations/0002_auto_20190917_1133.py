# Generated by Django 2.2.2 on 2019-09-17 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0008_teachingtask_is_changed'),
        ('teacher', '0006_teacher_photo'),
        ('headteacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='headteacher',
            options={'verbose_name': '班主任', 'verbose_name_plural': '班主任'},
        ),
        migrations.AddField(
            model_name='headteacher',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teachingtask.Semester'),
        ),
        migrations.AddField(
            model_name='headteacher',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.Teacher'),
        ),
    ]
