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
        ('archive.is', 'archive.is'),
        # ('webcitation.org', 'webcitation.org'),
    )
    archive = models.CharField(
        max_length=1000,
        choices=ARCHIVE_CHOICES,
        db_index=True,
        default=ARCHIVE_CHOICES[0][0],
    )
    url = models.URLField(max_length=1000)

    class Meta:
        ordering = ("-timestamp",)
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.url


@python_2_unicode_compatible
class Clip(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField(max_length=1000)
    mementos = models.ManyToManyField(Memento)

    def __str__(self):
        return self.url

    @property
    def timestamp(self):
        try:
            return self.mementos.get(archive="archive.org").timestamp
        except Memento.DoesNotExist:
            return self.mementos.latest().timestamp

    @property
    def ia_memento(self):
        try:
            return self.mementos.get(archive="archive.org")
        except Memento.DoesNotExist:
            return None
