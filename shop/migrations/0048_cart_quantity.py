# Generated by Django 4.0.4 on 2022-08-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0047_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]