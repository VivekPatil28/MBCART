# Generated by Django 4.0.4 on 2022-08-05 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0044_staticimages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StaticImages',
            new_name='StaticImage',
        ),
    ]