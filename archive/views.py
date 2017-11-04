# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import savepagenow
from .models import Clip, Memento
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
logger = logging.getLogger(__name__)


def index(request):
    context = {}
    if request.user.is_authenticated():
        clip_list = Clip.objects.filter(user=request.user).select_related("memento")
        context = {"clip_list": clip_list}
    return render(request, "archive/index.html", context)


def save(request):
    url = request.POST.get("url", None)
    if not url:
        return HttpResponseBadRequest("Bad request")

    user = request.user
    if not user.is_authenticated():
        return HttpResponseBadRequest("Bad request")

    logger.debug("Archiving {} for {}".format(url, user))
    memento_url, captured = savepagenow.capture_or_cache(url)

    logger.debug("Saving memento URL {}".format(memento_url))
    memento = Memento.objects.create(url=memento_url)
    clip = Clip.objects.create(
        user=user,
        url=url,
        memento=memento,
    )
    return redirect("/")
