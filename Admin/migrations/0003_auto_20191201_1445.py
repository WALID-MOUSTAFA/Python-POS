# Generated by Django 2.2.6 on 2019-12-01 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_auto_20191201_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='client',
            new_name='clien',
        ),
    ]
