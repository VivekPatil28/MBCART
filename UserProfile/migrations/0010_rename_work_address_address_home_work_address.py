# Generated by Django 4.0.4 on 2022-08-13 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0009_order_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='work_address',
            new_name='home_work_address',
        ),
    ]
