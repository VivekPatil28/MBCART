# Generated by Django 4.0.4 on 2022-08-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0049_cart_totalprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_desc',
            field=models.CharField(max_length=10000),
        ),
    ]
