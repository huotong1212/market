# Generated by Django 2.2 on 2019-06-21 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myresume', '0018_auto_20190621_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectation',
            name='resume_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expectation', to='myresume.UserResume', verbose_name='简历ID'),
        ),
    ]
