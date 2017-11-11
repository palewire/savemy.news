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


def delete(request):
    clip_id = request.POST.get("id", None)
    if not clip_id:
        logger.debug("No id")
        return HttpResponseBadRequest("Bad request: Clip ID not found")

    user = request.user
    if not user.is_authenticated():
        logger.debug("User not authenticated")
        return HttpResponseBadRequest("Bad request: User not authenticated")

    try:
        clip = Clip.objects.get(id=clip_id)
    except Clip.DoesNotExist:
        logger.debug("Clip {} does not exist".format(clip_id))
        return HttpResponseBadRequest("Bad request: Clip ID does not exist")

    if clip.user != user:
        logger.debug("Authenticated user is not owner of clip")
        return HttpResponseBadRequest("Bad request: User does not own clip")

    logger.debug("Deleting {} for {}".format(clip, user))
    clip.delete()

    return redirect("/")


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
