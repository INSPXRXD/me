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

__all__: typing.Sequence[str] = ("DjangoProjectRepository",)

import typing

from src.modules.portfolio.domain import project_repository
from src.modules.portfolio.infrastructure.persistence import models
from src.modules.portfolio.infrastructure.persistence import (
    project_mapper,
)

if typing.TYPE_CHECKING:
    from src.modules.portfolio.domain import project as project_
    from src.modules.portfolio.domain import (
        project_title as project_title_,
    )


class DjangoProjectRepository(project_repository.ProjectRepository):
    # << inherited docstring >>
    __slots__: typing.Sequence[str] = ("_mapper",)

    active_record = models.ProjectModel

    def __init__(self) -> None:
        self._mapper = project_mapper.ProjectMapper()

    def get_project(
        self, project_title: project_title_.ProjectTitle
    ) -> typing.Optional[project_.Project]:
        # << inherited docstring >>
        try:
            model = self.active_record.objects.get(title=project_title)
        except self.active_record.DoesNotExist:
            return None

        aggregate = self._mapper.model_to_entity(model)
        return aggregate

    def get_all_projects(
        self,
        *,
        filter_: typing.Optional[
            typing.Mapping[str, typing.Any]
        ] = None,
        order_by: typing.Optional[str] = None,
    ) -> typing.Sequence[project_.Project]:
        # << inherited docstring >>
        all_models = self.active_record.objects.all()
        if filter_ is not None:
            all_models = all_models.filter(**filter_)
        if order_by is not None:
            all_models = all_models.order_by(order_by)

        blogs = self._mapper.models_to_entities(all_models)
        return blogs

    def save(self, project: project_.Project) -> None:
        # << inherited docstring >>
        model = self._mapper.entity_to_model(project)
        self.active_record.save(model)
