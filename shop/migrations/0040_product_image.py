# Generated by Django 4.0.4 on 2022-07-31 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_remove_product_category_product_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='shop/thumbnail_image'),
        ),
    ]