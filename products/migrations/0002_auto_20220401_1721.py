# Generated by Django 3.1.7 on 2022-04-01 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created',), 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]
