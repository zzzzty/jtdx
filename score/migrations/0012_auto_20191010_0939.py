# Generated by Django 2.2.2 on 2019-10-10 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0011_auto_20190701_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.IntegerField(default='', null=True),
        ),
    ]
