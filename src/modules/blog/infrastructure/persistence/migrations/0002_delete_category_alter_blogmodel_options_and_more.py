# Generated by Django 4.1.4 on 2024-08-21 08:12
from __future__ import annotations

from django.db import migrations
from django.db import models

import src.modules.blog.domain.blog_category


class Migration(migrations.Migration):
    dependencies = [("blog", "0001_initial")]

    operations = [
        migrations.DeleteModel(name="Category"),
        migrations.AlterModelOptions(
            name="blogmodel", options={"get_latest_by": "time"}
        ),
        migrations.AlterField(
            model_name="blogmodel",
            name="category",
            field=models.CharField(
                choices=[
                    (
                        src.modules.blog.domain.blog_category.BlogCategory[
                            "UNCATEGORIZED"
                        ],
                        src.modules.blog.domain.blog_category.BlogCategory[
                            "UNCATEGORIZED"
                        ],
                    ),
                    (
                        src.modules.blog.domain.blog_category.BlogCategory[
                            "APPLICATION_ARCHITECT"
                        ],
                        src.modules.blog.domain.blog_category.BlogCategory[
                            "APPLICATION_ARCHITECT"
                        ],
                    ),
                ],
                default=src.modules.blog.domain.blog_category.BlogCategory[
                    "UNCATEGORIZED"
                ],
                max_length=255,
            ),
        ),
        migrations.AddIndex(
            model_name="blogmodel",
            index=models.Index(
                fields=["sno"], name="blog_blogmo_sno_7944ea_idx"
            ),
        ),
    ]
