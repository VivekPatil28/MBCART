# Generated by Django 4.0.4 on 2022-07-30 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_alter_reviewimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewimage',
            old_name='comment',
            new_name='review',
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
