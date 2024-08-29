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

__all__: typing.Sequence[str] = ("ProjectMapper",)

import typing

from src.modules.portfolio.domain import project
from src.modules.portfolio.domain import project_asset
from src.modules.portfolio.domain import project_content
from src.modules.portfolio.domain import project_reference
from src.modules.portfolio.domain import project_title
from src.modules.portfolio.infrastructure.persistence import (
    models as project_model,
)
from src.shared.infrastructure import mapper


class ProjectMapper(
    mapper.DataMapper[project.Project, project_model.ProjectModel]
):
    # << inherited docstring >>
    __slots__: typing.Sequence[str] = ()

    def model_to_entity(
        self, model: project_model.ProjectModel
    ) -> project.Project:
        # << inherited docstring >>
        entity = project.Project(
            title=project_title.ProjectTitle(model.title),
            asset=project_asset.ProjectAsset(
                thumbnail_url=model.thumbnail_url
            ),
            reference=project_reference.ProjectReference(
                demo_url=model.demo_url, github_url=model.github_url
            ),
            content=project_content.ProjectContent(
                description=model.description,
                technologies=model.technologies,
                features=model.features,
            ),
            created_at=model.date,
        )
        return entity

    def entity_to_model(
        self, entity: project.Project
    ) -> project_model.ProjectModel:
        # << inherited docstring >>
        model = project_model.ProjectModel(
            title=entity.title,
            description=entity.content.description,
            features=entity.content.features_list,
            thumbnail_url=entity.asset.thumbnail_url,
            demo_url=entity.reference.demo_url,
            github_url=entity.reference.github_url,
            date=entity.created_at,
        )
        return model
