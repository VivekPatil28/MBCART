# Generated by Django 4.1.7 on 2023-03-14 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0079_alter_reviewimage_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productdescriptionimages",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_desc_images",
                to="shop.product",
            ),
        ),
        migrations.AlterField(
            model_name="productimages",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_images",
                to="shop.product",
            ),
        ),
    ]