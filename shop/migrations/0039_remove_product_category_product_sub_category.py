# Generated by Django 4.0.4 on 2022-07-31 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='Sub_Category',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.DO_NOTHING, to='shop.subcategory'),
            preserve_default=False,
        ),
    ]
