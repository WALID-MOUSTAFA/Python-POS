# Generated by Django 2.2.6 on 2019-11-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_auto_20191118_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='name_ar',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='name_en',
            field=models.TextField(null=True),
        ),
    ]
