# Generated by Django 4.0.4 on 2022-12-30 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0016_alter_order_delivered_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='final_price',
            field=models.IntegerField(default=0),
        ),
    ]
