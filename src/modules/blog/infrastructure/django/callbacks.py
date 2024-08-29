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

__all__: typing.Sequence[str] = ("blog_created", "blog_deleted")

import contextlib
import typing

from django import dispatch
from django.db.models import signals

from src.config import container
from src.modules.blog.application.services import blog_streamer
from src.modules.blog.infrastructure.persistence import blog_mapper
from src.modules.blog.infrastructure.persistence import models
from src.shared.infrastructure import ioc
from src.shared.infrastructure.django import settings


@dispatch.receiver(signals.post_save, sender=models.BlogModel)
@ioc.inject
@typing.no_type_check
def blog_created(
    instance: models.BlogModel,
    created: bool,
    streamer: blog_streamer.BlogStreamerService = ioc.Provide[
        container.BlogContainer.blog_streamer,
    ],
    **_: typing.Any,
) -> None:
    """
    After creating a new blog model, it sends a corresponding
    signal, upon which the blog content is rendered into a
    static file of a specific format (e.g., PDF) using the
    appropriate service.
    """
    if settings.TESTING:
        # FIXME: Haven't come up with a better way to disable
        #        this functionality temporarily for testing
        #        purposes.
        return

    if created:
        mapper = blog_mapper.BlogMapper()
        domain_model = mapper.model_to_entity(instance)

        with contextlib.suppress(FileExistsError):
            # Generally, `builtins.FileExistsError` should not
            # be raised in this situation.
            #
            # `contextlib.suppress` is a precaution, as the
            # blog content might have been created for
            # some reason.
            streamer.init(domain_model)


@dispatch.receiver(signals.post_delete, sender=models.BlogModel)
@ioc.inject
@typing.no_type_check
def blog_deleted(
    instance: models.BlogModel,
    streamer: blog_streamer.BlogStreamerService = ioc.Provide[
        container.BlogContainer.blog_streamer,
    ],
    **_: typing.Any,
) -> None:
    """
    When a blog model is deleted, it sends a corresponding
    signal, upon which the static file containing the blog
    content is removed.
    """
    if settings.TESTING:
        # FIXME: Haven't come up with a better way to disable
        #        this functionality temporarily for testing
        #        purposes.
        return

    mapper = blog_mapper.BlogMapper()
    domain_model = mapper.model_to_entity(instance)

    with contextlib.suppress(FileNotFoundError):
        # Generally, `builtins.FileExistsError` should not be
        # raised in this situation.
        #
        # `contextlib.suppress` is a precaution, as the blog
        # content might have been removed for some reason
        # after initialization.
        streamer.delete(domain_model)
