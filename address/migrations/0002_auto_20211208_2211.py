# Generated by Django 3.2.9 on 2021-12-08 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['name'], 'verbose_name': 'District', 'verbose_name_plural': 'Districts'},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'ordering': ['name'], 'verbose_name': 'State', 'verbose_name_plural': 'States'},
        ),
    ]
