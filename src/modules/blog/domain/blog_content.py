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
"""A module containing the implementation of blog content."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("BlogContent",)

import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class BlogContent:
    """
    The content contained in the blog. This includes both
    meta-information about the blog and its title with text.
    """

    title: str
    meta: str
    content: str

    def __contains__(self, item: typing.Any) -> bool:
        if not isinstance(item, str):
            return NotImplemented
        return self.contains(item)

    def contains(
        self, item: str, *, case_sensitive: bool = False
    ) -> bool:
        """
        A method for searching for a specific word in the
        blog content (BlogContent) with an option for case
        sensitivity.

        Parameters
        ----------
        item: str
            The word to search for within the blog content.
        case_sensitive: bool
            If set to `builtins.True`, the search will be
            case-sensitive for the given word.
            Default `builtins.False`.

        Returns
        -------
        bool
            A boolean value indicating whether the specific word
            is present in the blog content.
        """
        contents: typing.Iterable[str] = (
            self.title,
            self.meta,
            self.content,
        )
        if not case_sensitive:
            item = item.lower()
            contents = map(str.lower, contents)

        for content in contents:
            if item in content:
                return True

        return False
