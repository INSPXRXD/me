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

__all__: typing.Sequence[str] = ("BlogMapper",)

import typing

from src.modules.blog.domain import blog
from src.modules.blog.domain import blog_asset
from src.modules.blog.domain import blog_category
from src.modules.blog.domain import blog_content
from src.modules.blog.domain import blog_id
from src.modules.blog.domain import blog_slug
from src.modules.blog.infrastructure.persistence import models
from src.shared.infrastructure import mapper


class BlogMapper(mapper.DataMapper[blog.Blog, models.BlogModel]):
    # << inherited docstring >>
    __slots__: typing.Sequence[str] = ()

    def entity_to_model(self, entity: blog.Blog) -> models.BlogModel:
        # << inherited docstring >>
        model = models.BlogModel(
            sno=entity.id,
            title=entity.content.title,
            meta=entity.content.meta,
            content=entity.content.content,
            thumbnail_url=entity.asset.thumbnail_url,
            category=str(entity.category),
            time=entity.created_at,
            slug=entity.slug,
        )
        return model

    def model_to_entity(self, model: models.BlogModel) -> blog.Blog:
        # << inherited docstring >>
        entity = blog.Blog(
            sno=blog_id.BlogId(model.sno),
            asset=blog_asset.BlogAsset(model.thumbnail_url),
            category=blog_category.BlogCategory(model.category),
            content=blog_content.BlogContent(
                title=model.title,
                meta=model.meta,
                content=model.content,
            ),
            created_at=model.time,
            slug=blog_slug.BlogSlug(model.slug),
        )
        return entity
