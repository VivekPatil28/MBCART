# Generated by Django 4.0.4 on 2023-01-19 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0069_alter_cart_quantity_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_techinical_details',
            field=models.TextField(default=' '),
        ),
    ]
