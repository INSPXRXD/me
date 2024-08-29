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

__all__: typing.Sequence[str] = ("TestDjangoProjectRepository",)

import typing

import pytest

from src.modules.portfolio.domain import project as project_
from src.modules.portfolio.domain import project_title as project_title_
from src.modules.portfolio.infrastructure.persistence import (
    project_repository as project_repository_impl,
)
from test_impl.portfolio import _util

if typing.TYPE_CHECKING:
    from src.modules.portfolio.domain import (
        project_repository as project_repository_,
    )


@pytest.fixture(name="project_repository")
def _() -> project_repository_.ProjectRepository:
    repo = project_repository_impl.DjangoProjectRepository()
    return repo


class TestDjangoProjectRepository:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_save_and_get_project(
        self, project_repository: project_repository_.ProjectRepository
    ) -> None:
        project_title = project_title_.ProjectTitle("1")

        project = project_repository.get_project(project_title)
        assert project is None

        entity = _util.project_from_title("1")
        project_repository.save(entity)

        project = project_repository.get_project(project_title)
        assert isinstance(project, project_.Project)

    @pytest.mark.django_db
    def test_get_all_blogs(
        self, project_repository: project_repository_.ProjectRepository
    ) -> None:
        projects = project_repository.get_all_projects()
        assert not projects

        entities = [
            _util.project_from_title(i)
            for i in [
                project_title_.ProjectTitle(str(_)) for _ in range(10)
            ]
        ]
        entities_count = len(entities)
        for entity in entities:
            project_repository.save(entity)

        projects = project_repository.get_all_projects()
        assert len(projects) == entities_count
        assert projects[0].title == project_title_.ProjectTitle("0")

        projects = project_repository.get_all_projects(
            order_by="-title"
        )
        assert projects[0].title == project_title_.ProjectTitle("9")
