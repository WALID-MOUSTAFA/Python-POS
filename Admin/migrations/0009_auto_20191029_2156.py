# Generated by Django 2.2.6 on 2019-10-29 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0008_auto_20191029_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(default='avatar.png', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='permission',
            field=models.ManyToManyField(null=True, to='Admin.Permission'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.Role'),
        ),
    ]
