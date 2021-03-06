# Generated by Django 3.2.9 on 2021-12-16 09:21

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import stores.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Category title')),
                ('is_active', models.BooleanField(default=True, help_text='Change category visibility', verbose_name='Is Active')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stores.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Product title')),
                ('description', models.TextField(blank=True, null=True)),
                ('sku', models.CharField(blank=True, help_text='Stock Keeping Unit', max_length=15, null=True, verbose_name='SKU')),
                ('regular_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99'}}, help_text='Maximum 99999999.99', max_digits=10, verbose_name='Regular price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99'}}, help_text='Maximum 99999999.99', max_digits=10, null=True, verbose_name='Discount price')),
                ('wholesale_price', models.DecimalField(blank=True, decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99'}}, help_text='Maximum 99999999.99', max_digits=10, null=True, verbose_name='Wholesale price')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('wholesale_min_quantity', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Change product visibility', verbose_name='Product visibility')),
                ('is_featured', models.BooleanField(default=False, help_text='Mark as featured product', verbose_name='Featured product')),
                ('is_downloadable', models.BooleanField(default=False, help_text='Mark as downloadable product')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='stores.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='vendor.vendor')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('value', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='stores.product')),
            ],
            options={
                'verbose_name': 'Specification',
                'verbose_name_plural': 'Specifications',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload a product image', upload_to=stores.models.upload_image_path, verbose_name='image')),
                ('alt_text', models.CharField(blank=True, max_length=100, null=True)),
                ('is_featured', models.BooleanField(default=False, help_text='Mark as featured image', verbose_name='Featured image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='stores.product')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ['-created_at'],
            },
        ),
    ]
