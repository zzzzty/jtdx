# Generated by Django 2.2.2 on 2019-06-24 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0006_auto_20190624_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachingtask',
            name='level',
        ),
    ]