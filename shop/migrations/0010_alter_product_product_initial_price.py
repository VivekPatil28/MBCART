# Generated by Django 4.0.4 on 2022-06-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_product_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_initial_price',
            field=models.FloatField(),
        ),
    ]
