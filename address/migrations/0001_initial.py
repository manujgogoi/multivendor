# Generated by Django 3.2.9 on 2021-12-16 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='District Name')),
                ('is_deliverable', models.BooleanField(default=True, help_text='Product deliverable or not', verbose_name='Is Deliverable')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PIN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='PIN code')),
                ('is_deliverable', models.BooleanField(default=True, help_text='Product deliverable or not', verbose_name='Is Deliverable')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pin_codes', to='address.district')),
            ],
            options={
                'verbose_name': 'PIN',
                'verbose_name_plural': 'PINs',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='State Name')),
                ('is_deliverable', models.BooleanField(default=True, help_text='Product deliverable or not', verbose_name='Is Deliverable')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='VillageOrTown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Village/Town Name')),
                ('is_deliverable', models.BooleanField(default=True, help_text='Product deliverable or not', verbose_name='Is Deliverable')),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='villages_or_towns', to='address.pin')),
            ],
            options={
                'verbose_name': 'village/Town',
                'verbose_name_plural': 'villages/Towns',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='address.state'),
        ),
    ]