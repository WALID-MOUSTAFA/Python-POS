# Generated by Django 2.2.6 on 2019-12-02 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_auto_20191202_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(through='Admin.Order_product', to='Admin.Product'),
        ),
    ]
