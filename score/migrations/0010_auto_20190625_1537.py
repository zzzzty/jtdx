# Generated by Django 2.2.2 on 2019-06-25 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0009_auto_20190624_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='task', to='teachingtask.TeachingTask'),
        ),
    ]
