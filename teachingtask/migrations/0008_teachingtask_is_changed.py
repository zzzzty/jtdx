# Generated by Django 2.2.2 on 2019-08-07 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0007_remove_teachingtask_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachingtask',
            name='is_changed',
            field=models.BooleanField(default=False),
        ),
    ]