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

__all__: typing.Sequence[str] = ("TestDjangoBlogRepository",)

import typing

import pytest

from src.modules.blog.domain import blog as blog_
from src.modules.blog.domain import blog_id as blog_id_
from src.modules.blog.infrastructure.persistence import (
    blog_repository as blog_repository_impl,
)
from test_impl.blog import _util

if typing.TYPE_CHECKING:
    from src.modules.blog.domain import (
        blog_repository as blog_repository_,
    )


@pytest.fixture(name="blog_repository")
def _() -> blog_repository_.BlogRepository:
    repo = blog_repository_impl.DjangoBlogRepository()
    return repo


class TestDjangoBlogRepository:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_save_and_get_blog(
        self, blog_repository: blog_repository_.BlogRepository
    ) -> None:
        blog_id = blog_id_.BlogId(1)

        blog = blog_repository.get_blog(blog_id)
        assert blog is None

        entity = _util.entity_from_id(blog_id)
        blog_repository.save(entity)

        blog = blog_repository.get_blog(blog_id)
        assert isinstance(blog, blog_.Blog)

    @pytest.mark.django_db
    def test_get_all_blogs(
        self, blog_repository: blog_repository_.BlogRepository
    ) -> None:
        blogs = blog_repository.get_all_blogs()
        assert not blogs

        entities = [
            _util.entity_from_id(i)
            for i in [blog_id_.BlogId(_) for _ in range(10)]
        ]
        entities_count = len(entities)
        for entity in entities:
            blog_repository.save(entity)

        blogs = blog_repository.get_all_blogs()
        assert len(blogs) == entities_count
        assert blogs[0].id == blog_id_.BlogId(0)

        blogs = blog_repository.get_all_blogs(order_by="-sno")
        assert blogs[0].id == blog_id_.BlogId(9)

        blogs = blog_repository.get_all_blogs(
            filter_={"sno__gte": blog_id_.BlogId(8)}
        )
        assert len(blogs) == 2
        assert blogs[0].id == blog_id_.BlogId(8)
