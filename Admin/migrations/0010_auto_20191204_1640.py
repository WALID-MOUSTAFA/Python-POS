# Generated by Django 2.2.6 on 2019-12-04 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0009_auto_20191204_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='order_product', through='Admin.Order_product', to='Admin.Product'),
        ),
    ]
