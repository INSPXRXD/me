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

__all__: typing.Sequence[str] = ("project_from_title",)

import datetime
import typing

from src.modules.portfolio.domain import project
from src.modules.portfolio.domain import project_asset
from src.modules.portfolio.domain import project_content
from src.modules.portfolio.domain import project_reference
from src.modules.portfolio.domain import project_title


def project_from_title(title: str) -> project.Project:
    entity = project.Project(
        title=project_title.ProjectTitle(title),
        asset=project_asset.ProjectAsset(thumbnail_url="https://"),
        reference=project_reference.ProjectReference(
            demo_url="https://", github_url="https://"
        ),
        content=project_content.ProjectContent(
            description="1", technologies="1", features="1"
        ),
        created_at=datetime.datetime.utcnow(),
    )
    return entity
