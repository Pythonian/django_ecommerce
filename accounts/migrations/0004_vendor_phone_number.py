# Generated by Django 3.1.7 on 2022-04-05 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220404_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='phone_number',
            field=models.CharField(default='', max_length=11),
            preserve_default=False,
        ),
    ]
