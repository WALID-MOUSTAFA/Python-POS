# Generated by Django 2.2.6 on 2019-11-18 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('desc_image', models.TextField(null=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('desc', models.TextField(null=True)),
            ],
            options={
                'db_table': 'permissions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sell_price', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.Category')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('desc', models.TextField(null=True)),
            ],
            options={
                'db_table': 'roles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product_images',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('iamge', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.Product')),
            ],
            options={
                'db_table': 'products_images',
            },
        ),
        migrations.CreateModel(
            name='Category_translation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('desc', models.TextField()),
                ('language', models.CharField(default='en', max_length=255)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.Category')),
            ],
            options={
                'db_table': 'category_translation',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.TextField(null=True)),
                ('fullname', models.TextField(null=True)),
                ('password', models.TextField(null=True)),
                ('email', models.TextField(null=True)),
                ('avatar', models.TextField(default='avatar.png', null=True)),
                ('register_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('permission', models.ManyToManyField(blank=True, related_name='permissions', to='Admin.Permission')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.Role')),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
    ]
