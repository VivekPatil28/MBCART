# Generated by Django 4.1.7 on 2023-04-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0089_remove_product_product_techinical_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_specifications",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
