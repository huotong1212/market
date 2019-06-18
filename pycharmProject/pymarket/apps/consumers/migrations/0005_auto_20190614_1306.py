# Generated by Django 2.2 on 2019-06-14 13:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0004_auto_20190614_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority',
            name='desc',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='权限描述'),
        ),
        migrations.AlterField(
            model_name='authority',
            name='role',
            field=models.ManyToManyField(blank=True, null=True, related_name='authority', to='consumers.Role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='desc',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='角色描述'),
        ),
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
    ]
