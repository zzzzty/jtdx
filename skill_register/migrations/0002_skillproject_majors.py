# Generated by Django 2.2.2 on 2019-11-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('major', '0001_initial'),
        ('skill_register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillproject',
            name='majors',
            field=models.ManyToManyField(to='major.Major'),
        ),
    ]