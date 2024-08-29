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

__all__: typing.Sequence[str] = ("DataMapper",)

import abc
import typing

_EntityT = typing.TypeVar("_EntityT")
_ModelT = typing.TypeVar("_ModelT")


class DataMapper(typing.Generic[_EntityT, _ModelT], abc.ABC):
    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    def model_to_entity(self, model: _ModelT) -> _EntityT: ...

    @abc.abstractmethod
    def entity_to_model(self, entity: _EntityT) -> _ModelT: ...

    def models_to_entities(
        self, models: typing.Iterable[_ModelT]
    ) -> typing.Sequence[_EntityT]:
        entities = [self.model_to_entity(m) for m in models]
        return entities

    def entities_to_models(
        self, entities: typing.Iterable[_EntityT]
    ) -> typing.Sequence[_ModelT]:
        models = [self.entity_to_model(e) for e in entities]
        return models
