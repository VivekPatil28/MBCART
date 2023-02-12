# Generated by Django 4.0.4 on 2022-12-30 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0013_address_default_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='UserProfile.address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='shipped_date',
            field=models.DateField(default=False),
        ),
    ]