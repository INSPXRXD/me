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
"""A module containing the implementation of the domain aggregate Blog."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("Blog",)

import datetime
import typing
import unicodedata

from src.modules.blog.domain import blog_slug

if typing.TYPE_CHECKING:
    from src.modules.blog.domain import blog_asset
    from src.modules.blog.domain import blog_category
    from src.modules.blog.domain import blog_content
    from src.modules.blog.domain import blog_id


class Blog:
    """
    An aggregate that ensures the integrity of blog data
    and manages its state. The Blog adheres to certain
    invariants, such as the format of the created slug,
    which is set automatically if not explicitly provided.

    Parameters
    ----------
    sno: BlogId
        The serial number of the blog, serving as its unique
        identifier. The blog number can only be of a numeric type.
    content: BlogContent
        The content contained in the blog. This includes both
        meta-information about the blog and its title with text.
    asset: BlogAsset
        An object containing content related to the media
        representation of the blog, such as a cover image and more.
    category: BlogCategory
        The category of the blog, which is the topic on which
        the blog is written.
    created_at: datetime
        The time when the blog was published.
    slug: Optional[BlogSlug]
        A short label for the blog, containing only letters, numbers,
        underscores, or hyphens. With regard to certain invariants
        maintained within this aggregate.

        Default `builtins.None`.
    """

    __slots__: typing.Sequence[str] = (
        "_id",
        "_slug",
        "_content",
        "_asset",
        "_category",
        "_created_at",
    )

    def __init__(
        self,
        sno: blog_id.BlogId,
        content: blog_content.BlogContent,
        asset: blog_asset.BlogAsset,
        category: blog_category.BlogCategory,
        created_at: datetime.datetime,
        slug: typing.Optional[blog_slug.BlogSlug] = None,
    ) -> None:
        self._id = sno
        self._content = content
        self._asset = asset
        self._category = category
        self._created_at = created_at

        if slug is None:
            slug = self.make_slug()

        self._slug = slug

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Blog):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return self.id

    @property
    def id(self) -> blog_id.BlogId:
        """
        The serial number of the blog, serving as its unique
        identifier. The blog number can only be of a numeric type.
        """
        return self._id

    @property
    def slug(self) -> blog_slug.BlogSlug:
        """
        A short label for the blog, containing only letters,
        numbers, underscores, or hyphens. With regard to certain
        invariants maintained within this aggregate.
        """
        return self._slug

    @property
    def content(self) -> blog_content.BlogContent:
        """
        The content contained in the blog. This includes both
        meta-information about the blog and its title with text.
        """
        return self._content

    @property
    def asset(self) -> blog_asset.BlogAsset:
        """
        An object containing content related to the media
        representation of the blog, such as a cover image and more.
        """
        return self._asset

    @property
    def category(self) -> blog_category.BlogCategory:
        """
        The category of the blog, which is the topic on which the
        blog is written.
        """
        return self._category

    @property
    def created_at(self) -> datetime.datetime:
        """The time when the blog was published."""
        return self._created_at

    def contains_word(
        self, word: str, *, case_sensitive: bool = False
    ) -> bool:
        """
        A method to search for a specific word within the blog
        content (BlogContent) with an option for case sensitivity.

        Parameters
        ----------
        word: str
            The word to search for within the blog content.
        case_sensitive: bool
            If set to `builtins.True`, the search will be
            case-sensitive for the given word.
            Default `builtins.False`.

        Returns
        -------
        bool
            A boolean value indicating whether the specific word
            is present in the blog content.
        """
        contains = self.content.contains(
            word, case_sensitive=case_sensitive
        )
        return contains

    def make_slug(self) -> blog_slug.BlogSlug:
        """
        Generates a slug based on the blog's title. In accordance
        with the established design invariants, Unicode
        normalization is used to remove diacritical marks and
        convert to ASCII.

        Info
        ----
        Since the Blog aggregate has a unique identifier in the
        form of a serial number, by design, the slug does not need
        to be unique across all blogs.

        This property was implemented for more human-readable
        links generated at the infrastructure level.

        Returns
        -------
        BlogSlug
            A short label for the blog, containing only letters,
            numbers, underscores, or hyphens. With regard to certain
            invariants maintained within this aggregate.
        """
        # TODO: Is this a meaningful part of the Blog aggregate?
        #       See test_impl/blog/domain/blog.feature
        slug = "-".join(
            _
            for _ in (
                unicodedata.normalize("NFKD", self._content.title)
                .encode("ascii", "ignore")
                .decode("ascii")
                .lower()
                .split(" ")
            )
            if _
        )
        return blog_slug.BlogSlug(slug)

    def edit(
        self,
        *,
        content: typing.Optional[blog_content.BlogContent] = None,
        asset: typing.Optional[blog_asset.BlogAsset] = None,
        category: typing.Optional[blog_category.BlogCategory] = None,
    ) -> None:
        """
        Allows editing of certain parameters of the blog after
        its creation. Thus, it is the only point in the aggregate
        where the blog content can be modified.

        Parameters
        ----------
        content: Optional[BlogContent]
            The content contained in the blog. This includes both
            meta-information about the blog and its title with text.
        asset: Optional[BlogAsset]
            An object containing content related to the media
            representation of the blog, such as a cover image and more.
        category: Optional[BlogCategory]
            The category of the blog, which is the topic on which
            the blog is written.
        """
        if content is not None:
            self._content = content
        if asset is not None:
            self._asset = asset
        if category is not None:
            self._category = category
