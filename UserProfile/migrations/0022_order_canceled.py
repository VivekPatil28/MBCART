# Generated by Django 4.1.7 on 2023-02-24 05:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("UserProfile", "0021_alter_order_order_id_alter_order_payment_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="canceled",
            field=models.BooleanField(default=False),
        ),
    ]