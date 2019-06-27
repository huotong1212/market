# Generated by Django 2.2 on 2019-06-19 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myresume.models


class Migration(migrations.Migration):

    dependencies = [
        ('myresume', '0010_auto_20190618_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresume',
            name='name',
            field=models.CharField(help_text='简历名称', max_length=200, verbose_name='简历名称'),
        ),
        migrations.AlterField(
            model_name='userresume',
            name='portrait',
            field=models.ImageField(blank=True, null=True, upload_to=myresume.models.upload_to, verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='userresume',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='userresume',
            name='username',
            field=models.CharField(blank=True, help_text='姓名', max_length=20, null=True, verbose_name='姓名'),
        ),
    ]