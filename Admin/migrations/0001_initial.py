# Generated by Django 2.2.6 on 2019-10-27 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('fullname', models.TextField()),
                ('password', models.TextField()),
                ('email', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
