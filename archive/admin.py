# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Clip, Memento


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ("url", "user", "timestamp", "memento_count")
    search_fields = ("user", "url")
    readonly_fields = ["user", "url", "mementos"]


@admin.register(Memento)
class MementoAdmin(admin.ModelAdmin):
    list_display = ("url", "timestamp",)
    list_filter = ("archive",)
    readonly_fields = ("url", "archive", "timestamp")


admin.site.site_header = 'Save My News'
admin.site.site_title = 'Save My News'
