# Generated by Django 2.2.2 on 2019-09-17 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_auto_20190807_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='classes.Classes')),
            ],
        ),
    ]