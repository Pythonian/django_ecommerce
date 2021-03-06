# Generated by Django 3.1.7 on 2022-04-06 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20220406_1350'),
        ('orders', '0004_order_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vendors',
            field=models.ManyToManyField(related_name='orders', to='accounts.Vendor'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='accounts.vendor'),
        ),
    ]
