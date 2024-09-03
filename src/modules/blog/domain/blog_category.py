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
"""A module containing the implementation of the blog category."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("BlogCategory",)

import enum
import typing


class BlogCategory(str, enum.Enum):
    """
    The category of the blog, which is the topic on which
    the blog is written.
    """

    _generate_next_value_: typing.Any = staticmethod(
        lambda n, *_: n.lower().replace("_", "-")
    )
    # "SOME_CATEGORY" will be transformed into "some-category".

    UNCATEGORIZED = enum.auto()
    """
    A category not related to anything else. Set when the 
    blog's topic is not defined for some reason.
    """

    APPLICATION_ARCHITECT = enum.auto()
    """
    A theme related to corporate application templates, 
    various patterns, and approaches in business 
    application design.
    """

    def __str__(self) -> str:
        return str(self.value)
