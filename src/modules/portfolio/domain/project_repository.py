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

__all__: typing.Sequence[str] = ("ProjectRepository",)

import abc
import typing

if typing.TYPE_CHECKING:
    from src.modules.portfolio.domain import project as project_
    from src.modules.portfolio.domain import (
        project_title as project_title_,
    )


class ProjectRepository(abc.ABC):
    """
    A repository representing a collection of Project
    aggregate objects. The repository can filter and
    return results based on application requirements.
    """

    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    def get_project(
        self, project_title: project_title_.ProjectTitle
    ) -> typing.Optional[project_.Project]:
        """
        Returns a project object by its unique identifier.

        Parameters
        ----------
        project_title : ProjectTitle
            The unique identifier of the project to be
            searched for.

        Returns
        -------
        Optional[Project]
            The Project object if found, or `builtins.None`
            if a project with the specified identifier does
            not exist.
        """
        ...

    @abc.abstractmethod
    def get_all_projects(
        self,
        *,
        filter_: typing.Optional[
            typing.Mapping[str, typing.Any]
        ] = None,
        order_by: typing.Optional[str] = None,
    ) -> typing.Sequence[project_.Project]:
        """
        Returns a list of all projects, with options for
        filtering and sorting based on specified parameters.

        Parameters
        ----------
        filter_ : Optional[Mapping[str, Any]]
            A dictionary with filtering criteria. The dictionary
            keys may correspond to attributes of the Project
            object, and the values are filtering conditions (e.g.,
            category, creation date). If `builtins.None`, no
            filtering is applied.

            Default is `builtins.None`.
        order_by : Optional[str], optional
            The field by which to sort the results. If
            `builtins.None`, no sorting is applied.

            Default is `builtins.None`.

        Returns
        -------
        Sequence[Project]
            A list of Project objects that match the specified
            filtering and sorting conditions.
        """
        ...

    @abc.abstractmethod
    def save(self, project: project_.Project) -> None:
        """
        Saves a project object in the repository. If a project
        with the given identifier already exists, it will be
        updated; otherwise, a new object will be created.

        Parameters
        ----------
        project : Project
            The Project object to be saved or updated in the
            repository.
        """
        ...
