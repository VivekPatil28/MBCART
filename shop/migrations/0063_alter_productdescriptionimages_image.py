# Generated by Django 4.0.4 on 2022-09-01 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0062_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdescriptionimages',
            name='image',
            field=models.ImageField(default='shop/media/placeholder.png', upload_to='shop/DescImages'),
        ),
    ]