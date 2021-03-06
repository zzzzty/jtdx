# Generated by Django 2.2.2 on 2019-07-29 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('content', models.CharField(max_length=20)),
                ('filepath', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '文件上传',
                'verbose_name_plural': '文件上传',
                'ordering': ('-create_time',),
            },
        ),
    ]
