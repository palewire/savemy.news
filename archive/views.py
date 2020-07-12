# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import logging
import savepagenow
from .tasks import ia_memento
from .models import Clip, Memento
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
logger = logging.getLogger(__name__)


def index(request):
    """
    The homepage. Personalized if you're logged in.
    """
    context = {'clip_list': None}
    # If the user is logged in ...
    if request.user.is_authenticated:
        # ... query their clips
        clip_list = Clip.objects.filter(user=request.user).prefetch_related("mementos")
        context['clip_list'] = clip_list
    return render(request, "archive/index.html", context)


def download(request):
    """
    Lets logged in users download their clips.
    """
    user = request.user
    if not user.is_authenticated:
        logger.debug("User not authenticated")
        return HttpResponseBadRequest("Bad request: User not authenticated")

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clips.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'source_url', 'timestamp', 'archive_url', 'archive_url'])
    clip_list = Clip.objects.filter(user=user).prefetch_related("mementos")
    for clip in clip_list:
        row = [clip.id, clip.url, clip.timestamp]
        for m in clip.mementos.all():
            row.append(m.url)
        writer.writerow(row)
    return response


def delete(request):
    """
    Lets logged in users delete clips.
    """
    clip_id = request.POST.get("id", None)
    if not clip_id:
        logger.debug("No id")
        return HttpResponseBadRequest("Bad request: Clip ID not found")

    user = request.user
    if not user.is_authenticated:
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
    """
    Saves a URL with the Wayback Machine.
    """
    # Verify there is a URL to save
    url = request.POST.get("url", None)
    if not url:
        return HttpResponseBadRequest("Bad request")

    # Verify the user is logged in
    user = request.user
    if not user.is_authenticated:
        return HttpResponseBadRequest("Bad request")

    # Sent URL to Internet Archive
    # This is required so we throw an error if it fails
    logger.debug("Archiving {} for {}".format(url, user))

    # Write it all to the database
    clip = Clip.objects.create(user=user, url=url)

    # Trigger an archiving task with archive.org
    ia_memento.delay(clip.id)

    # Head back where the user started
    return redirect("/")


def status(request):
    """
    Some stats about the site.
    """
    context = {
        'user_count': User.objects.count(),
        'clip_count': Clip.objects.count(),
        'memento_count': Memento.objects.count(),
        'archiveorg_count': Memento.objects.filter(archive='archive.org').count(),
        'archiveis_count': Memento.objects.filter(archive='archive.is').count(),
        'webcitation_count': Memento.objects.filter(archive='webcitation.org').count(),
    }
    return render(request, "archive/status.html", context)
