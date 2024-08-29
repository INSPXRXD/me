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

__all__: typing.Sequence[str] = ("TestBlogStreamerService",)

import contextlib
import io
import os
import pathlib
import typing

import pytest

from src.config import dirs
from src.modules.blog.application.services import (
    blog_streamer as blog_streamer_,
)
from src.modules.blog.domain import blog_id as blog_id_
from src.shared.infrastructure.django import settings
from test_impl.blog import _util


@contextlib.contextmanager
def simulate_production_mode_for_blog_streams(
    blogs_root: os.PathLike,
) -> typing.Iterator[None]:
    settings.TESTING = False
    yield
    settings.TESTING = True

    for source in os.listdir(blogs_root):
        if source.endswith(".pdf"):
            file_path = os.path.join(blogs_root, source)
            if os.path.exists(file_path):
                os.remove(file_path)


@pytest.fixture(name="blog_streamer")
def _() -> blog_streamer_.BlogStreamerService:
    streamer = blog_streamer_.BlogStreamerService(root=dirs.BLOGS_DIR)
    return streamer


class TestBlogStreamerService:
    __slots__: typing.Sequence[str] = ()

    def test_raises_if_root_dir_does_not_exist(self) -> None:
        with pytest.raises(NotADirectoryError):
            blog_streamer_.BlogStreamerService(
                root=pathlib.Path("/does/not/exist")
            )

    def test_init_and_open_stream(
        self, blog_streamer: blog_streamer_.BlogStreamerService
    ) -> None:
        with simulate_production_mode_for_blog_streams(
            blog_streamer._root
        ):
            blog_id = blog_id_.BlogId(1)
            entity = _util.entity_from_id(blog_id)

            stream_id = blog_streamer._create_id(entity)

            source = os.path.join(blog_streamer._root, stream_id)
            assert not os.path.exists(source)

            blog_streamer.init(entity)
            assert os.path.exists(source)

            stream = blog_streamer.open(entity)
            assert isinstance(stream, io.BufferedReader)

            # We are not in the Django env and no one will close it for us.
            stream.close()

    def test_delete_stream(
        self, blog_streamer: blog_streamer_.BlogStreamerService
    ) -> None:
        blog_id = blog_id_.BlogId(1)
        entity = _util.entity_from_id(blog_id)

        stream_id = blog_streamer._create_id(entity)

        source = os.path.join(blog_streamer._root, stream_id)
        assert not os.path.exists(source)

        blog_streamer.init(entity)
        assert os.path.exists(source)

        blog_streamer.delete(entity)
        assert not os.path.exists(source)
