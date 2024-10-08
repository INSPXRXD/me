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
# mypy: ignore-errors
from __future__ import annotations

__all__: typing.Sequence[str] = ("BlogAdmin", "BlogAdminForm")

import typing

from django import forms
from django.contrib import admin

from src.modules.blog.infrastructure.persistence import models


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"id": "richtext_field"})
    )

    class Meta:
        model = models.BlogModel
        fields = "__all__"


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(models.BlogModel, BlogAdmin)
