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

__all__: typing.Sequence[str] = ("TestBlogMapper",)

import datetime
import typing

import pytest

from src.modules.blog.domain import blog
from src.modules.blog.domain import blog_asset
from src.modules.blog.domain import blog_category
from src.modules.blog.domain import blog_content
from src.modules.blog.domain import blog_id
from src.modules.blog.domain import blog_slug
from src.modules.blog.infrastructure.persistence import (
    blog_mapper as blog_mapper_,
)
from src.modules.blog.infrastructure.persistence import models


@pytest.fixture(name="blog_mapper")
def _() -> blog_mapper_.BlogMapper:
    mapper = blog_mapper_.BlogMapper()
    return mapper


class TestBlogMapper:
    __slots__: typing.Sequence[str] = ()

    def test_entity_to_model(
        self, blog_mapper: blog_mapper_.BlogMapper
    ) -> None:
        entity = blog.Blog(
            sno=blog_id.BlogId(1),
            content=blog_content.BlogContent(
                title="1", meta="1", content="1"
            ),
            asset=blog_asset.BlogAsset(thumbnail_url="1"),
            category=blog_category.BlogCategory.UNCATEGORIZED,
            slug=blog_slug.BlogSlug("1"),
            created_at=datetime.datetime.utcnow(),
        )

        model = blog_mapper.entity_to_model(entity)
        assert isinstance(model, models.BlogModel)

    def test_model_to_entity(
        self, blog_mapper: blog_mapper_.BlogMapper
    ) -> None:
        model = models.BlogModel(
            sno=1,
            title="1",
            meta="1",
            content="1",
            thumbnail_url="https://1.jpg",
            category="uncategorized",
            time=datetime.datetime.utcnow(),
            slug="1",
        )

        entity = blog_mapper.model_to_entity(model)
        assert isinstance(entity, blog.Blog)
