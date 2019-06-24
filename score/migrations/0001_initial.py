# Generated by Django 2.2 on 2019-06-17 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('teachingtask', '0001_initial'),
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_changed', models.BooleanField(default=False)),
                ('make_up', models.IntegerField(default=1)),
                ('is_make_up_input', models.BooleanField(default=False)),
                ('make_up_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.Teacher')),
                ('root', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_comment', to='score.Score')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.Student')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teachingtask.TeachingTask')),
            ],
            options={
                'unique_together': {('task', 'student', 'root', 'make_up')},
            },
        ),
        migrations.CreateModel(
            name='Change_Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass_order', models.BooleanField(default=False)),
                ('change_to', models.IntegerField(default=0)),
                ('changescore', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='score.Score')),
            ],
        ),
    ]