# Generated by Django 2.2.2 on 2019-08-05 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemaster', '0002_auto_20190805_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docfile',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='docfile',
            name='filepath',
            field=models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/', verbose_name='下载'),
        ),
        migrations.AlterField(
            model_name='docfile',
            name='name',
            field=models.CharField(max_length=20, verbose_name='名称'),
        ),
    ]
