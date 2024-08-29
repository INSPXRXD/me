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

__all__: typing.Sequence[str] = ("TestIndexView",)

import typing

import pytest
from django import test
from django import urls
from pytest_django import asserts

from src.modules.portfolio.infrastructure.django import views


class TestIndexView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/")
        response = views.index(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("portfolio:home"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("portfolio:home"))
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "index.html")


class TestAboutView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/about")
        response = views.about(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("portfolio:about"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("portfolio:about"))
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "portfolio/about.html")


class TestProjectsView:
    __slots__: typing.Sequence[str] = ()

    @pytest.mark.django_db
    def test_view_url_exists_at_desired_location(
        self, rf: test.RequestFactory
    ) -> None:
        request = rf.get("/projects")
        response = views.projects(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_url_accessible_by_name(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("portfolio:projects"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_view_uses_correct_template(
        self, client: test.Client
    ) -> None:
        response = client.get(urls.reverse("portfolio:projects"))
        assert response.status_code == 200

        asserts.assertTemplateUsed(response, "portfolio/projects.html")
