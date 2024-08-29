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

__all__: typing.Sequence[str] = ("ProjectContent",)

import dataclasses
import typing


def _split_by_comma(string_values: str) -> typing.List[str]:
    list_values = list(map(str.strip, string_values.split(",")))
    return list_values


@dataclasses.dataclass(frozen=True)
class ProjectContent:
    """
    The content of the project, including the description,
    technologies used, and the project's features.
    """

    description: str
    technologies: str
    features: typing.Optional[str] = None

    @property
    def features_list(self) -> typing.List[str]:
        """A list of features used in the project."""
        features = self.features if self.features is not None else ""
        return _split_by_comma(features)

    @property
    def technologies_list(self) -> typing.List[str]:
        """
        A list of technologies used to create the project.
        """
        return _split_by_comma(self.technologies)
