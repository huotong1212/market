# Generated by Django 2.2 on 2019-06-02 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_hotsearchwords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='goods.GoodCategory', verbose_name='商品类别'),
        ),
        migrations.CreateModel(
            name='IndexAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='goods.GoodCategory', verbose_name='商品类目')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='goods.Goods')),
            ],
            options={
                'verbose_name': '首页商品类别广告',
                'verbose_name_plural': '首页商品类别广告',
            },
        ),
    ]
