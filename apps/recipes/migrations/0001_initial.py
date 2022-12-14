# Generated by Django 4.1.2 on 2022-10-19 20:51

import versatileimagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Recipe title")),
                (
                    "image",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        null=True,
                        upload_to="recipe_images/",
                        verbose_name="Recipe image",
                    ),
                ),
                ("description", models.TextField(verbose_name="Recipe description")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date created"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Date updated")),
            ],
            options={
                "ordering": ("title",),
            },
        ),
    ]
