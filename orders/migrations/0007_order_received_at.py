# Generated by Django 4.0.1 on 2022-02-01 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_delivery_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
