import logging
import archiveis
import webcitation
from celery.decorators import task
from archive.models import Memento, Clip
logger = logging.getLogger(__name__)


@task()
def is_memento(clip_id):
    clip = Clip.objects.get(id=clip_id)
    logger.debug("Archiving {} with archive.is".format(clip.url))
    from archivenow import archivenow
    try:
        is_url = archiveis.capture(clip.url)
        # is_url = archivenow.push(clip.url, "is")[0]
        is_memento = Memento.objects.create(url=is_url, archive="archive.is")
        logger.debug("Created {}".format(is_memento))
        clip.mementos.add(is_memento)
    except Exception as e:
        logger.debug("archive.is failed")
        logger.debug(e)


@task()
def wc_memento(clip_id):
    clip = Clip.objects.get(id=clip_id)
    logger.debug("Archiving {} with webcitation".format(clip.url))
    try:
        wc_url = webcitation.capture(clip.url)
        wc_memento = Memento.objects.create(url=wc_url, archive="webcitation.org")
        logger.debug("Created {}".format(wc_memento))
        clip.mementos.add(wc_memento)
    except Exception as e:
        logger.debug("webcitation failed")
        logger.debug(e)
