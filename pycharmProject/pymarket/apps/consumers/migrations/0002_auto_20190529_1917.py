# Generated by Django 2.2 on 2019-05-29 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerprofile',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='出生年月'),
        ),
    ]