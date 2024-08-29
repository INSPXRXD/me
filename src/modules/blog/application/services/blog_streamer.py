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
A module that contains a service linking specific logic of the domain
aggregate Blog and infrastructure implementations for interacting with
the file system.
"""

from __future__ import annotations

__all__: typing.Sequence[str] = ("BlogStreamerService",)

import os
import typing

if typing.TYPE_CHECKING:
    from src.modules.blog.domain import blog as blog_


def _create_blog_source_stub(
    root: os.PathLike[str], stream_id: str
) -> None:
    # Creates a readable PDF placeholder file for a specific blog.
    # TODO : Implement full translation of the blog text, taking
    #        into account markdown.
    # FIXME: The logic for translating the blog text into a specific
    #        format should be handled by the corresponding implementation
    #        in the infrastructure layer, not the application layer.

    header = b"%PDF-1.0\n"
    page = (
        b"1 0 obj\n<</Type /Page\n/Parent 2 0 R\n"
        b"/Resources << /Font << /F1 3 0 R >> >>\n"
        b"/Contents 4 0 R\n>>\nendobj\n"
    )
    font = (
        b"3 0 obj\n<</Type /Font\n/BaseFont /Helvetica\n"
        b">>\nendobj\n"
    )
    content = (
        b"4 0 obj\n"
        b"<</Length " + str(len(stream_id)).encode() + b">>\n"
        b"stream\n" + stream_id.encode() + b"\nendstream\n"
        b"endobj\n"
    )
    page_tree = (
        b"2 0 obj\n<</Type /Pages\n/Kids [1 0 R]\n"
        b"/Count 1\n>>\nendobj\n"
    )
    catalog = (
        b"1 0 obj\n<</Type /Catalog\n/Pages 2 0 R\n" b">>\nendobj\n"
    )
    xref_offset = sum(
        map(len, (header, page, font, content, page_tree, catalog))
    )
    xref = (
        b"xref\n0 " + str(6).encode() + b"\n"
        b"0000000000 65535 f \n0000000000 65535 f \n"
        b"0000000000 65535 f \n0000000000 65535 f \n"
        b"0000000000 65535 f \n0000000000 65535 f \n"
    )
    trailer = (
        b"trailer\n"
        b"<</Size 6 /Root 1 0 R /Info 5 0 R>>\n"
        b"startxref\n" + str(xref_offset).encode() + b"\n"
        b"%%EOF\n"
    )

    with open(os.path.join(root, stream_id), "wb") as blog_source_stub:
        blog_source_stub.write(
            (
                header
                + page
                + font
                + content
                + page_tree
                + catalog
                + xref
                + trailer
            )
        )


class BlogStreamerService:
    """
    Service that interacts with the domain aggregate Blog,
    implementing the logic to translate blog content into
    a file of the corresponding format (currently supports PDF).

    Parameters
    ----------
    TODO: Should accept a specific implementation that
          contains the logic for translating blog text into
          the corresponding file type, and also refer to a
          common abstraction.

    root: PathLike
        The path to the directory where the blogs should
        be translated.

    Raises
    ------
    NotADirectoryError
        If a non-existent directory is provided for blog
        translation.
    """

    __slots__: typing.Sequence[str] = ("_root",)

    def __init__(self, root: os.PathLike[str]) -> None:
        if not os.path.exists(root):
            raise NotADirectoryError(
                f"The {root!r} directory does not exist."
            )
        self._root = root

    @staticmethod
    def _create_id(blog: blog_.Blog) -> str:
        stream_id = f"{blog.id}-{blog.slug}.pdf"
        return stream_id

    def open(self, blog: blog_.Blog) -> typing.BinaryIO:
        """
        Creates a file translation containing the blog content.

        Note
        ----
        If the blog translation is used in a context where
        automatic closure is not provided, you will need to
        close it manually.

        Parameters
        ----------
        blog: Blog
            The blog that needs to be translated.
        """
        stream_id = self._create_id(blog)
        stream = open(os.path.join(self._root, stream_id), "rb")
        return stream

    def delete(self, blog: blog_.Blog) -> None:
        """
        Deletes the already saved translation for a specific
        blog, based on the previously set directory.

        Parameters
        ----------
        blog: Blog
            The blog whose content needs to be deleted.
        """
        stream_id = self._create_id(blog)
        os.remove(os.path.join(self._root, stream_id))

    def init(self, blog: blog_.Blog) -> None:
        """
        Initializes the blog content in the previously set
        directory.

        Parameters
        ----------
        blog: Blog
            The blog whose content needs to be initialized.

        Raises
        ------
        FileExistsError
            If content for this blog has already been
            initialized.
        """
        stream_id = self._create_id(blog)
        if os.path.exists(os.path.join(self._root, stream_id)):
            raise FileExistsError(
                f"The blog source {stream_id!r} already exists."
            )

        # FIXME: stub
        _create_blog_source_stub(self._root, stream_id)
