# Generated by Django 2.2 on 2019-06-20 22:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myresume', '0013_auto_20190620_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='enrollment_date',
            field=models.DateField(default=datetime.date.today, verbose_name='入学日期'),
        ),
        migrations.AlterField(
            model_name='education',
            name='graduate_date',
            field=models.DateField(default=datetime.date.today, verbose_name='毕业日期'),
        ),
        migrations.AlterField(
            model_name='projectexperience',
            name='end_time',
            field=models.DateField(default=datetime.date.today, verbose_name='结束日期'),
        ),
        migrations.AlterField(
            model_name='projectexperience',
            name='start_time',
            field=models.DateField(default=datetime.date.today, verbose_name='起始日期'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='company',
            field=models.CharField(blank=True, default='公司名称', max_length=30, null=True, verbose_name='任职公司'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='end_time',
            field=models.DateField(default=datetime.date.today, verbose_name='结束日期'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='start_time',
            field=models.DateField(default=datetime.date.today, verbose_name='起始日期'),
        ),
    ]