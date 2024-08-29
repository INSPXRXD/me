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
    "ProjectModel",
    "SkillModel",
    "SkillType",
    "SkillCategory",
    "SkillGradient",
    "AboutMeModel",
)

import collections
import reprlib
import string
import typing
import uuid

from django.db import models


class ProjectModel(models.Model):  # type: ignore[misc]
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300)
    features = models.TextField(null=True, blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    technologies = models.CharField(max_length=300)
    demo_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class SkillGradient(models.TextChoices):  # type: ignore[misc]
    BLUE = "from-cyan-300 to-blue-400"
    LIGHT_BLUE = "from-white to-blue-400"

    RED = "from-red-300 to-red-600"
    LIGHT_RED = "from-white to-red-300"

    PURPLE = "from-pink-400 to-purple-400"
    LIGHT_PURPLE = "from-white to-purple-400"


class SkillCategory(models.Model):  # type: ignore[misc]
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    gradient = models.TextField(choices=SkillGradient.choices)

    def __str__(self) -> str:
        return self.name


class SkillType(models.Model):  # type: ignore[misc]
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    gradient = models.TextField(choices=SkillGradient.choices)

    def __str__(self) -> str:
        return self.name


class SkillModel(models.Model):  # type: ignore[misc]
    name = models.CharField(max_length=200)
    rate = models.IntegerField(
        blank=0, null=False, default=0, verbose_name="Rate (out of 100)"
    )
    tag = models.CharField(
        blank=True, null=False, default="", max_length=200
    )
    type = models.ForeignKey(
        SkillType,
        blank=False,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    category = models.ForeignKey(
        SkillCategory,
        blank=False,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    gradient = models.TextField(choices=SkillGradient.choices)

    def __str__(self) -> str:
        return self.name

    def clamp_rate(self) -> None:
        self.rate = min(100, max(0, self.rate))

    def save(self, *args: typing.Any) -> None:
        self.tag = "".join(
            c.lower()
            for c in self.name
            if c.lower() in string.ascii_lowercase
        )
        if not self.tag:
            self.tag = uuid.uuid4().hex

        self.tag = self.tag.replace(" ", "_")
        self.clamp_rate()
        return super().save(*args)


class AboutMeModel(models.Model):  # type: ignore[misc]
    name = models.CharField(
        blank=True, null=False, default="", max_length=30
    )
    text = models.TextField(blank=True, null=False, default="")
    skills = models.ManyToManyField(
        SkillModel, blank=True, related_name="skills_about"
    )

    def __str__(self) -> str:
        return reprlib.repr(self.text)

    @classmethod
    def actual(cls) -> typing.Optional[AboutMeModel]:
        return cls.objects.first()

    def group_skills(
        self,
    ) -> typing.ItemsView[
        typing.Any,
        typing.DefaultDict[typing.Any, typing.List[typing.Any]],
    ]:
        grouped: typing.DefaultDict[
            SkillType,
            typing.DefaultDict[SkillCategory, typing.List[SkillModel]],
        ] = collections.defaultdict(
            lambda: collections.defaultdict(list)
        )
        for skill in self.skills.all():
            grouped[skill.type][skill.category].append(skill)

        grouped = typing.cast(
            typing.DefaultDict[
                typing.Any,
                typing.DefaultDict[typing.Any, typing.List[typing.Any]],
            ],
            {
                k: v.items()  # SkillType  # [SkillCategory, List[Skill]]
                for k, v in grouped.items()
            },
        )
        return grouped.items()
