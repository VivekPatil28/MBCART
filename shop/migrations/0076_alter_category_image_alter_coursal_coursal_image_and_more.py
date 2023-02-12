# Generated by Django 4.0.4 on 2023-02-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0075_alter_productdescriptionimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='Category_thumbnail'),
        ),
        migrations.AlterField(
            model_name='coursal',
            name='coursal_image',
            field=models.ImageField(default='', upload_to='coursal_images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='thumbnail_image'),
        ),
        migrations.AlterField(
            model_name='productdescriptionimages',
            name='image',
            field=models.ImageField(default='', upload_to='DescImages'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(default='', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='reviewimage',
            name='image',
            field=models.ImageField(upload_to='Reviewimages'),
        ),
        migrations.AlterField(
            model_name='staticimage',
            name='image',
            field=models.ImageField(upload_to='static'),
        ),
    ]
