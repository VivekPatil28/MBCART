# Generated by Django 4.0.4 on 2023-02-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0074_alter_category_image_alter_coursal_coursal_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdescriptionimages',
            name='image',
            field=models.ImageField(default='', upload_to='media/DescImages'),
        ),
    ]
