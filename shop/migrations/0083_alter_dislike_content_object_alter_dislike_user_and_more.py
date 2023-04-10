# Generated by Django 4.1.7 on 2023-04-01 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0082_remove_reviewimage_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dislike",
            name="content_object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dcontentobject",
                to="shop.review",
            ),
        ),
        migrations.AlterField(
            model_name="dislike",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="duser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="content_object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lcontentobject",
                to="shop.review",
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="luser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
