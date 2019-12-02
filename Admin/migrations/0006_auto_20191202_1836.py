# Generated by Django 2.2.6 on 2019-12-02 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_order_product_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_product',
            name='created_date',
        ),
        migrations.AddField(
            model_name='order',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
