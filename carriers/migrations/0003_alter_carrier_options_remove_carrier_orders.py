# Generated by Django 4.0.1 on 2022-02-06 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carriers', '0002_carrier_landmark_alter_carrier_last_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrier',
            options={'ordering': ['first_name'], 'verbose_name': 'Carrier', 'verbose_name_plural': 'Carriers'},
        ),
        migrations.RemoveField(
            model_name='carrier',
            name='orders',
        ),
    ]
