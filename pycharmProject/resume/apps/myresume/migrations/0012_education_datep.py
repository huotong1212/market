# Generated by Django 2.2 on 2019-06-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myresume', '0011_auto_20190619_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='dateP',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='日期区间'),
        ),
    ]