# Generated by Django 4.0.1 on 2022-02-16 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carriers', '0004_carrier_address_proof_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='address_proof_number',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='address_proof_type',
            field=models.CharField(choices=[('AD', 'Aadhaar Card'), ('PP', 'Passport'), ('BP', 'Bank Passbook')], max_length=2),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='id_proof_number',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='id_proof_type',
            field=models.CharField(choices=[('PN', 'PAN Card'), ('AD', 'Aadhaar Card'), ('PP', 'Passport'), ('DL', 'Driving License')], max_length=2),
        ),
    ]
