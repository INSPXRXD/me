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
"""
A module that contains all the containers for all other modules of
the application (src.modules.X). The containers are used to implement
the IoC approach in this project to reduce coupling and shift from
concrete implementations to abstractions.
"""

# mypy: ignore-errors
from __future__ import annotations

__all__: typing.Sequence[str] = ("BlogContainer", "PortfolioContainer")

import typing

from dependency_injector import containers
from dependency_injector import providers

from src.config import dirs
from src.modules.blog.application.services import blog_streamer
from src.modules.blog.infrastructure.persistence import (
    blog_repository as blog_repository_impl,
)
from src.modules.portfolio.infrastructure.persistence import (
    project_repository as project_repository_impl,
)

if typing.TYPE_CHECKING:
    from src.modules.blog.domain import (
        blog_repository as blog_repository_,
    )
    from src.modules.portfolio.domain import (
        project_repository as project_repository_,
    )


class BlogContainer(containers.DeclarativeContainer):
    blog_repository: blog_repository_.BlogRepository = (
        providers.Singleton(blog_repository_impl.DjangoBlogRepository)
    )
    """A repository that uses the Blog aggregate as its model."""

    blog_streamer: blog_streamer.BlogStreamerService = (
        providers.Factory(
            blog_streamer.BlogStreamerService, root=dirs.BLOGS_DIR
        )
    )
    """A service that allows creating blog views in PDF format."""


class PortfolioContainer(containers.DeclarativeContainer):
    project_repository: project_repository_.ProjectRepository = (
        providers.Singleton(
            project_repository_impl.DjangoProjectRepository
        )
    )
    """A repository that uses the Project aggregate as its model."""
