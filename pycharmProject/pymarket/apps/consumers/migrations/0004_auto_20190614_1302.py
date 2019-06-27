# Generated by Django 2.2 on 2019-06-14 13:02

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0003_auto_20190531_1432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verifycode',
            options={'verbose_name': '验证码', 'verbose_name_plural': '验证码'},
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='角色名称')),
                ('desc', models.CharField(max_length=200, verbose_name='角色描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.ManyToManyField(related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户角色',
                'verbose_name_plural': '用户角色',
            },
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='权限名称')),
                ('desc', models.CharField(max_length=200, verbose_name='权限描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('role', models.ManyToManyField(related_name='authority', to='consumers.Role')),
            ],
            options={
                'verbose_name': '用户权限',
                'verbose_name_plural': '用户权限',
            },
        ),
    ]