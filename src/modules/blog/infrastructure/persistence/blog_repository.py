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

__all__: typing.Sequence[str] = ("DjangoBlogRepository",)

import typing

from src.modules.blog.domain import blog_repository
from src.modules.blog.infrastructure.persistence import blog_mapper
from src.modules.blog.infrastructure.persistence import models

if typing.TYPE_CHECKING:
    from src.modules.blog.domain import blog as blog_
    from src.modules.blog.domain import blog_id as blog_id_


class DjangoBlogRepository(blog_repository.BlogRepository):
    # << inherited docstring >>
    __slots__: typing.Sequence[str] = ("_mapper",)

    active_record = models.BlogModel

    def __init__(self) -> None:
        self._mapper = blog_mapper.BlogMapper()

    def get_blog(
        self, blog_id: blog_id_.BlogId
    ) -> typing.Optional[blog_.Blog]:
        # << inherited docstring >>
        try:
            model = self.active_record.objects.get(sno=blog_id)
        except self.active_record.DoesNotExist:
            return None

        aggregate = self._mapper.model_to_entity(model)
        return aggregate

    def get_all_blogs(
        self,
        *,
        filter_: typing.Optional[
            typing.Mapping[str, typing.Any]
        ] = None,
        order_by: typing.Optional[str] = None,
    ) -> typing.Sequence[blog_.Blog]:
        # << inherited docstring >>
        all_models = self.active_record.objects.all()
        if filter_ is not None:
            all_models = all_models.filter(**filter_)
        if order_by is not None:
            all_models = all_models.order_by(order_by)

        blogs = self._mapper.models_to_entities(all_models)
        return blogs

    def save(self, blog: blog_.Blog) -> None:
        # << inherited docstring >>
        model = self._mapper.entity_to_model(blog)
        self.active_record.save(model)
