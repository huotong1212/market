# Generated by Django 2.2 on 2019-06-17 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myresume', '0008_auto_20190617_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectation',
            name='salary_max',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='薪资范围'),
        ),
    ]