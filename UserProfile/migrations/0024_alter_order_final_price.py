# Generated by Django 4.1.7 on 2023-02-24 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("UserProfile", "0023_alter_order_delivered_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="final_price",
            field=models.IntegerField(default=0, editable=False),
        ),
    ]