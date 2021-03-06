# Generated by Django 4.0.4 on 2022-06-26 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Clothing', 'Clothing'), ('Electronics', 'Electronics'), ('Mobiles', 'Mobiles'), ('Laptop', 'Laptop'), ('Washing Machines', 'Washing Machines'), ('Computers', 'Computers'), ('Smart Watches', 'Smart Watches'), ('Toys', 'Toys'), ('Air Coolers', 'Air Coolers'), ('Headphones', 'Headphones'), ('Water Purifiers', 'Water Purifiers'), ('Trimmers', 'Trimmers'), ('Deodrants', 'Deodrants'), ('Anrivirous', 'Anrivirous'), ('Wallets', 'Wallets'), ('Fans', 'Fans'), ('Camera', 'Camera'), ('Deodorants', 'Deodorants'), ('College Bags', 'College Bags'), ('Laptop Bags', 'Laptop Bags'), ('Televisions', 'Televisions')], max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_initial_price',
            field=models.IntegerField(),
        ),
    ]
