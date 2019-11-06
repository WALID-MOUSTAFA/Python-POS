# Generated by Django 2.2.6 on 2019-11-01 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_auto_20191030_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='permission',
        ),
        migrations.AddField(
            model_name='permission',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user', to='Admin.User'),
        ),
    ]
