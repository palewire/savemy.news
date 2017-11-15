# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Memento(models.Model):
    timestamp = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
    )
    ARCHIVE_CHOICES = (
        ('archive.org', 'archive.org'),
        # ('archive.is', 'archive.is'),
        # ('webcitation.org', 'webcitation.org'),
    )
    archive = models.CharField(
        max_length=1000,
        choices=ARCHIVE_CHOICES,
        db_index=True,
        default=ARCHIVE_CHOICES[0][0],
    )
    url = models.URLField()

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return self.url


@python_2_unicode_compatible
class Clip(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    memento = models.ForeignKey(Memento, related_name="old_memento")
    mementos = models.ManyToManyField(Memento)

    class Meta:
        ordering = ("-memento__timestamp",)

    def __str__(self):
        return self.url

    @property
    def timestamp(self):
        return self.memento.timestamp
