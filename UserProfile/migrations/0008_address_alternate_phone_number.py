# Generated by Django 4.0.4 on 2022-08-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0007_rename_address_type_address_work_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='alternate_phone_number',
            field=models.CharField(default=552, max_length=20),
            preserve_default=False,
        ),
    ]
