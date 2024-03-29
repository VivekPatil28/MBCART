# Generated by Django 4.0.4 on 2022-08-11 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0056_staticimage_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('shipped', models.BooleanField(default=False)),
                ('shipped_date', models.DateField()),
                ('outfordelivery', models.BooleanField(default=False)),
                ('outfordelivery_date', models.DateField()),
                ('delivered', models.BooleanField(default=False)),
                ('delivered_date', models.DateField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
