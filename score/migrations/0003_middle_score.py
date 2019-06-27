# Generated by Django 2.2.2 on 2019-06-24 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20190624_1626'),
        ('score', '0002_auto_20190624_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Middle_Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[(1, '期末'), (2, '开学补考'), (3, '重修'), (4, '毕业前清考'), (5, '毕业后清考'), (6, '最后一次')], max_length=10, null=True)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.Teacher')),
                ('which_score', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='score.Score')),
            ],
        ),
    ]