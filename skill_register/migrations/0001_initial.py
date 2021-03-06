# Generated by Django 2.2.2 on 2019-11-18 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SkillProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='skillproject/%Y/%m/%d/')),
                ('context', models.CharField(blank=True, max_length=50, null=True)),
                ('skilltype', models.CharField(max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_sell', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '技能大赛项目',
                'verbose_name_plural': '技能大赛项目',
                'ordering': ('create_time', 'is_sell'),
            },
        ),
    ]
