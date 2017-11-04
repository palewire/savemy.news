# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Clip, Memento


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ("url", "user", "timestamp")


@admin.register(Memento)
class MementoAdmin(admin.ModelAdmin):
    list_display = ("url", "timestamp",)
