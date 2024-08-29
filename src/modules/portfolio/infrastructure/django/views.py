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

__all__: typing.Sequence[str] = ("index", "about", "projects")

import typing

from django import http
from django import shortcuts

from src.config import container
from src.modules.blog.domain import blog_repository as blog_repository_
from src.modules.portfolio.domain import (
    project_repository as project_repository_,
)
from src.modules.portfolio.infrastructure.persistence import models
from src.shared.infrastructure import ioc


@ioc.inject
def index(
    request: http.HttpRequest,
    repo: blog_repository_.BlogRepository = ioc.Provide[
        container.BlogContainer.blog_repository,
    ],
) -> http.HttpResponse:
    response = shortcuts.render(
        request, "index.html", {"latest_blogs": repo.get_all_blogs()}
    )
    return response


def about(request: http.HttpRequest) -> http.HttpResponse:
    cv = models.AboutMeModel.actual()
    if cv is None:
        empty_cv = shortcuts.render(request, "portfolio/about.html", {})
        return empty_cv

    cv = shortcuts.render(
        request,
        "portfolio/about.html",
        {
            "cv_text": cv.text,
            "cv_name": cv.name,
            "cv_skills": cv.group_skills(),
        },
    )
    return cv


@ioc.inject
def projects(
    request: http.HttpRequest,
    repo: project_repository_.ProjectRepository = ioc.Provide[
        container.PortfolioContainer.project_repository,
    ],
) -> http.HttpResponse:
    response = shortcuts.render(
        request,
        "portfolio/projects.html",
        {"projects": repo.get_all_projects()},
    )
    return response
