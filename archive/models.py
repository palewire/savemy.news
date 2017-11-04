# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


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

    def __unicode__(self):
        return self.url


class Clip(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    memento = models.ForeignKey(Memento)

    class Meta:
        ordering = ("-memento__timestamp",)

    @property
    def timestamp(self):
        return self.memento.timestamp
