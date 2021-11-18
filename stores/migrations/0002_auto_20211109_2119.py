# Generated by Django 3.2.9 on 2021-11-09 15:49

from django.db import migrations, models
import stores.models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Change category visibility', verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(help_text='Upload a product image', upload_to=stores.models.upload_image_path, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
