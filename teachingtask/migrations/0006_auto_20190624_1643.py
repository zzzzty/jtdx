# Generated by Django 2.2.2 on 2019-06-24 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachingtask', '0005_teachingtask_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachingtask',
            name='level',
            field=models.IntegerField(choices=[(1, '期末'), (2, '开学补考'), (3, '重修'), (4, '毕业前清考'), (5, '毕业后清考'), (6, '最后一次')], null=True),
        ),
    ]
