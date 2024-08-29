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
    "TestBlogView",
    "TestSearchView",
    "TestBlogpostView",
    "TestCategoryView",
    "TestCategoriesView",
)

import datetime
import typing
from unittest import mock

import pytest
from django import test
from django import urls
from pytest_django import asserts

from src.modules.blog.infrastructure.django import views


class TestBlogView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/blog")
        response = views.blog(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("blog:blog"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("blog:blog"))
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "blog/blog.html")


class TestCategoryView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/category")
        response = views.category(request, category="awesome_category")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(
            urls.reverse("blog:category", kwargs={"category": "_"})
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(
            urls.reverse("blog:category", kwargs={"category": "_"})
        )
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "blog/category.html")


class TestCategoriesView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/categories")
        response = views.categories(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("blog:categories"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("blog:categories"))
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "blog/categories.html")


class TestSearchView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/search")
        response = views.search(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("blog:search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("blog:search"))
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "blog/search.html")

    @pytest.mark.django_db
    def test_search_no_query(self, rf: test.RequestFactory) -> None:
        request = rf.get("/search")
        response = views.search(request)
        assert response.status_code == 200
        assert b"No query provided." in response.content

    @pytest.mark.django_db
    def test_search_with_no_results(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/search", {"q": "nonexistent"})

        response = views.search(request)
        assert response.status_code == 200
        assert (
            b"Sorry, no results found for your search query."
            in response.content
        )

    @pytest.mark.django_db
    def test_search_with_results(self, rf: test.RequestFactory) -> None:
        blog1 = mock.Mock()
        blog1.contains_word.return_value = True
        blog1.created_at = datetime.datetime.utcnow()
        blog1.title = "Blog Title 1"

        blog2 = mock.Mock()
        blog2.contains_word.return_value = True
        blog2.created_at = (
            datetime.datetime.utcnow() + datetime.timedelta(days=1)
        )
        blog2.title = "Blog Title 2"

        mock_repo = mock.Mock()
        mock_repo.get_all_blogs.return_value = [blog1, blog2]

        request = rf.get("/search", {"q": "test"})
        response = views.search(request, repo=mock_repo)
        assert response.status_code == 200

        assert b"Blog Title 1" in response.content
        assert b"Blog Title 2" in response.content

        assert b"Read more" in response.content


class TestBlogpostView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/blogpost")
        response = views.blogpost(request, id=1, slug="2")
        assert response.status_code == 404

        blogpost_mock = mock.Mock()
        blogpost_mock.id = 1
        blogpost_mock.slug = "2"

        repo_mock = mock.Mock()
        repo_mock.get_blog.return_value = blogpost_mock

        response = views.blogpost(
            request,
            id=blogpost_mock.id,
            slug=blogpost_mock.slug,
            repo=repo_mock,
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(
            urls.reverse("blog:blogpost", args=[1, "2"])
        )
        assert response.status_code == 404
