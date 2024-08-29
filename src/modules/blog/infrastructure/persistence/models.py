# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2024 INSPXRXD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

__all__: typing.Sequence[str] = ("BlogModel",)

import typing

from django.db import models

from src.modules.blog.domain import blog_category


class BlogModel(models.Model):  # type: ignore[misc]
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    meta = models.CharField(max_length=300)
    content = models.TextField()
    thumbnail_url = models.URLField(blank=True, null=True)
    category = models.CharField(
        max_length=255,
        default=blog_category.BlogCategory.UNCATEGORIZED,
        choices=[(_, _) for _ in list(blog_category.BlogCategory)],
    )
    time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        blank=True,
        null=True,
        max_length=40,
        unique=False,  # For identification, we use SNO.
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [models.Index(fields=["sno"])]
        get_latest_by = "time"
