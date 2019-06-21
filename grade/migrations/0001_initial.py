# Generated by Django 2.2 on 2019-06-17 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='年级名称')),
            ],
            options={
                'verbose_name': '年级',
                'verbose_name_plural': '年级',
            },
        ),
    ]
