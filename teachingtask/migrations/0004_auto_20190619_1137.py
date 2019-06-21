# Generated by Django 2.2 on 2019-06-19 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0003_auto_20190617_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='child_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_semesters', to='teachingtask.Semester'),
        ),
        migrations.AddField(
            model_name='semester',
            name='root_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_semesters', to='teachingtask.Semester'),
        ),
    ]
