# Generated by Django 4.0.4 on 2022-08-09 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_alter_product_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticimage',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.category'),
            preserve_default=False,
        ),
    ]
