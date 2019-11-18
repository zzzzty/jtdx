# Generated by Django 2.2.2 on 2019-11-18 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0008_teachingtask_is_changed'),
        ('student', '0003_auto_20190924_1210'),
        ('skill_register', '0002_skillproject_majors'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillChoose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teachingtask.Semester')),
                ('skillproject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='skill_register.SkillProject')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.Student')),
            ],
            options={
                'verbose_name': '技能大赛报名信息',
                'verbose_name_plural': '技能大赛报名信息',
            },
        ),
    ]