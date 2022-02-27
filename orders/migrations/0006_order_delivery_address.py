# Generated by Django 3.2.9 on 2022-01-07 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20220105_1038'),
        ('orders', '0005_alter_order_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user_profile.deliveryaddress'),
        ),
    ]