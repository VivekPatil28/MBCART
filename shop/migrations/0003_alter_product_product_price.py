# Generated by Django 4.0.4 on 2022-06-21 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(),
        ),
    ]