# Generated by Django 4.0.4 on 2022-06-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_remove_coursal_id_coursal_coursal_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Clothing', 'Clothing'), ('Electronics', 'Electronics'), ('Mobiles', 'Mobiles'), ('Laptops', 'Laptops'), ('Washing Machines', 'Washing Machines'), ('Computers', 'Computers'), ('Smart Watches', 'Smart Watches'), ('Toys', 'Toys'), ('Air Coolers', 'Air Coolers'), ('Headphones', 'Headphones'), ('Water Purifiers', 'Water Purifiers'), ('Trimmers', 'Trimmers'), ('Deodrants', 'Deodrants'), ('Anrivirous', 'Anrivirous'), ('Wallets', 'Wallets'), ('Fans', 'Fans'), ('Camera', 'Camera'), ('Deodorants', 'Deodorants'), ('College Bags', 'College Bags'), ('Laptop Bags', 'Laptop Bags'), ('Televisions', 'Televisions')], default=1, max_length=100),
            preserve_default=False,
        ),
    ]
