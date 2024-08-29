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

__all__: typing.Sequence[str] = (
    "test_checking_for_presence_of_content_in_its_attributes",
)

import ast
import typing

import pytest_bdd as ts
from hamcrest import assert_that
from hamcrest import is_
from pytest_bdd import parsers


@ts.scenario(
    "blog_content.feature",
    "Checking for presence of content in its attributes",
)
def test_checking_for_presence_of_content_in_its_attributes() -> None:
    pass


@ts.given(
    parsers.parse(
        "{title}, {meta}, and {content} attributes of the blog content"
    ),
    target_fixture="blog_content_attributes",
)
def _(title: str, meta: str, content: str) -> typing.Mapping[str, str]:
    attributes = {"title": title, "meta": meta, "content": content}
    return attributes


@ts.when(
    parsers.parse(
        "we check if the blog content contains the string {string}"
    ),
    target_fixture="expected_result",
)
def _(
    blog_content_attributes: typing.Mapping[str, str], string: str
) -> bool:
    expected_result = any(
        string in value for value in blog_content_attributes.values()
    )
    return expected_result


@ts.then(
    parsers.parse(
        "the corresponding boolean value {contains} is returned"
    )
)
def _(expected_result: bool, contains: str) -> None:
    assert_that(expected_result, is_(ast.literal_eval(contains)))
