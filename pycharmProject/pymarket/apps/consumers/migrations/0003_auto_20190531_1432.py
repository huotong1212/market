# Generated by Django 2.2 on 2019-05-31 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0002_auto_20190529_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号'),
        ),
    ]