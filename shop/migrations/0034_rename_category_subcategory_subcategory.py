# Generated by Django 4.0.4 on 2022-07-31 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_rename_cateogory_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='category',
            new_name='SubCategory',
        ),
    ]
