# Generated by Django 4.0.1 on 2022-02-06 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0008_rename_completed_order_delivered_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('house_no', models.CharField(blank=True, max_length=20, null=True, verbose_name='House No')),
                ('vill_or_town', models.CharField(blank=True, max_length=50, null=True, verbose_name='Village / Town')),
                ('district', models.CharField(blank=True, max_length=50, null=True, verbose_name='District')),
                ('state', models.CharField(blank=True, max_length=50, null=True, verbose_name='State')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='Country')),
                ('pin_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='PIN Code')),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile No')),
                ('mobile_verified', models.BooleanField(default=False, verbose_name='Is mobile verified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('id_proof_type', models.CharField(choices=[('PAN', 'PAN Card'), ('AADHAAR', 'Aadhaar Card'), ('PASSPORT', 'Passport'), ('DRIVING_LICENSE', 'other')], max_length=20)),
                ('id_proof_number', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('address_proof_type', models.CharField(choices=[('AADHAAR', 'Aadhaar Card'), ('PASSPORT', 'Passport'), ('BANK_PASSBOOK', 'Bank Passbook')], max_length=20)),
                ('address_proof_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('orders', models.ManyToManyField(to='orders.Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carriers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
