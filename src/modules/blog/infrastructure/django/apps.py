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

__all__: typing.Sequence[str] = ("BlogConfig",)

import importlib
import typing

from django import apps
from django.core import signals


class BlogConfig(apps.AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.blog"

    def _load_packages(self) -> None:
        """
        Load additional modules like admin.py, that Django
        does not see in this directory.
        """
        # TODO: Maybe there's a better way to load files like admin.py?
        #       For example, specifying a custom path somewhere... ?
        importlib.import_module(
            "src.modules.blog.infrastructure.django.admin"
        )

    def _connect_callbacks(self) -> None:
        from src.modules.blog.infrastructure.django import callbacks

        for callback_name in callbacks.__all__:
            callback = typing.cast(
                typing.Callable[..., typing.Any],
                getattr(callbacks, callback_name, None),
            )
            if callback is not None:
                signals.setting_changed.connect(callback)

    def ready(self) -> None:
        from src.modules.blog.infrastructure import container

        container.blog_container.wire(
            modules=[
                "src.modules.blog.infrastructure.django.views",
                "src.modules.blog.infrastructure.django.callbacks",
                "src.modules.portfolio.infrastructure.django.views",
            ]
        )
        self._load_packages()
        self._connect_callbacks()
