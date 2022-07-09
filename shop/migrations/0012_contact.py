# Generated by Django 4.0.4 on 2022-06-24 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_remove_product_product_initial_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50)),
                ('phoneNumber', models.IntegerField(max_length=10)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
    ]
