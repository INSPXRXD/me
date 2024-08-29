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

__all__: typing.Sequence[str] = (
    "blog",
    "category",
    "categories",
    "search",
    "blogpost",
)

import operator
import typing

from django import http
from django import shortcuts
from django.core import paginator as paginator_

from src.config import container
from src.modules.blog.application.services import blog_streamer
from src.modules.blog.domain import blog_id
from src.modules.blog.domain import blog_repository as blog_repository_
from src.shared.infrastructure import ioc


@ioc.inject
def blog(
    request: http.HttpRequest,
    repo: blog_repository_.BlogRepository = ioc.Provide[
        container.BlogContainer.blog_repository,
    ],
) -> http.HttpResponse:
    paginator = paginator_.Paginator(repo.get_all_blogs(), 3)
    blogs = paginator.get_page(request.GET.get("page"))

    response = shortcuts.render(
        request, "blog/blog.html", {"blogs": blogs}
    )
    return response


@ioc.inject
def category(
    request: http.HttpRequest,
    category: str,
    repo: blog_repository_.BlogRepository = ioc.Provide[
        container.BlogContainer.blog_repository,
    ],
) -> http.HttpResponse:
    posts = repo.get_all_blogs(
        filter_=dict(category=category), order_by="-time"
    )
    if not posts:
        response = shortcuts.render(
            request,
            "blog/category.html",
            {"message": f"No posts found in category: {category!r}"},
        )
        return response

    paginator = paginator_.Paginator(posts, 3)
    posts = paginator.get_page(request.GET.get("page"))

    response = shortcuts.render(
        request,
        "blog/category.html",
        {"category": category, "category_posts": posts},
    )
    return response


@ioc.inject
def categories(
    request: http.HttpRequest,
    repo: blog_repository_.BlogRepository = ioc.Provide[
        container.BlogContainer.blog_repository,
    ],
) -> http.HttpResponse:
    all_categories = typing.cast(typing.List[str], [])
    all_categories.extend(
        set(b.category.value for b in repo.get_all_blogs())
    )
    all_categories.sort()

    response = shortcuts.render(
        request,
        "blog/categories.html",
        {"all_categories": all_categories},
    )
    return response


@ioc.inject
@typing.no_type_check
def search(
    request,
    repo: blog_repository_.BlogRepository = ioc.Provide[
        container.BlogContainer.blog_repository,
    ],
) -> http.HttpResponse:
    query = request.GET.get("q")
    if query is None:
        response = shortcuts.render(
            request,
            "blog/search.html",
            {
                "results": [],
                "query": query,
                "message": "No query provided.",
            },
        )
        return response

    blogs = repo.get_all_blogs()
    results = []
    for word in query.split():
        matching_blogs = [
            blog for blog in blogs if blog.contains_word(word)
        ]
        if matching_blogs:
            matching_blogs.sort(key=operator.attrgetter("created_at"))
            results.extend(matching_blogs)

    paginator = paginator_.Paginator(results, 3)
    results = paginator.get_page(request.GET.get("page"))

    response = shortcuts.render(
        request,
        "blog/search.html",
        {
            "results": results,
            "query": query,
            "message": (
                ""
                if results
                else "Sorry, no results found for your search query.",
            ),
        },
    )
    return response


@ioc.inject
def blogpost(
    request: http.HttpRequest,
    id: int,
    slug: str,
    repo: blog_repository_.BlogRepository = ioc.Provide[
        container.BlogContainer.blog_repository,
    ],
    streamer: blog_streamer.BlogStreamerService = ioc.Provide[
        container.BlogContainer.blog_streamer,
    ],
) -> typing.Union[http.HttpResponse, http.FileResponse]:
    blog = repo.get_blog(blog_id.BlogId(id))
    if blog is None:
        response = shortcuts.render(
            request,
            "404.html",
            {"message": "Blog post not found"},
            status=404,
        )
        return response

    if request.GET.get("format", "html") == "html":
        response = shortcuts.render(
            request, "blog/blogpost.html", {"blog": blog}
        )
        return response

    try:
        response = http.FileResponse(
            streamer.open(blog), content_type="application/pdf"
        )
        return response

    except FileNotFoundError:
        response = shortcuts.render(
            request,
            "404.html",
            {"message": "Blog post source not found"},
            status=404,
        )
        return response
