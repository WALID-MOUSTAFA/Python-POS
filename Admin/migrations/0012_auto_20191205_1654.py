# Generated by Django 2.2.6 on 2019-12-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_auto_20191204_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(through='Admin.Order_product', to='Admin.Product'),
        ),
    ]
