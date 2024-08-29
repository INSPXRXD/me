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

__all__: typing.Sequence[str] = ("Project",)

import datetime
import typing

if typing.TYPE_CHECKING:
    from src.modules.portfolio.domain import project_asset
    from src.modules.portfolio.domain import project_content
    from src.modules.portfolio.domain import project_reference
    from src.modules.portfolio.domain import project_title


class Project:
    """
    An aggregate that ensures the integrity of project data
    and manages its state.

    Parameters
    ----------
    title: ProjectTitle
        The title of the project, which serves as its unique
        identifier.
    content: ProjectContent
        The content of the project, including description,
        technologies used, and the project's features.
    asset: ProjectAsset
        Media resources associated with the project, such as
        images, videos, or other files used for the visual
        representation of the project.
    reference: ProjectReference
        External links or other reference materials that may
        be useful for the project's context. For example, a
        link to a project demo.
    created_at: datetime
        The date and time the project was created.
    """

    # FIXME: Currently, the model is anemic
    __slots__: typing.Sequence[str] = (
        "_content",
        "_asset",
        "_reference",
        "_created_at",
        "_title",
    )

    def __init__(
        self,
        title: project_title.ProjectTitle,
        content: project_content.ProjectContent,
        asset: project_asset.ProjectAsset,
        reference: project_reference.ProjectReference,
        created_at: datetime.datetime,
    ) -> None:
        self._title = title
        self._content = content
        self._asset = asset
        self._reference = reference
        self._created_at = created_at

    @property
    def title(self) -> project_title.ProjectTitle:
        """
        The title of the project, which serves as its unique
        identifier.
        """
        return self._title

    @property
    def content(self) -> project_content.ProjectContent:
        """
        The content of the project, including description,
        technologies used, and the project's features.
        """
        return self._content

    @property
    def asset(self) -> project_asset.ProjectAsset:
        """
        Media resources associated with the project, such
        as images, videos, or other files used for the visual
        representation of the project.
        """
        return self._asset

    @property
    def reference(self) -> project_reference.ProjectReference:
        """
        External links or other reference materials that may
        be useful for the project's context. For example, a
        link to a project demo.
        """
        return self._reference

    @property
    def created_at(self) -> datetime.datetime:
        """The date and time the project was created."""
        return self._created_at
