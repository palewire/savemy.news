import logging
import archiveis
import webcitation
import savepagenow
from celery.decorators import task
from archive.models import Memento, Clip
logger = logging.getLogger(__name__)


@task()
def ia_memento(clip_id):
    """
    Archive a clip with archive.org
    """
    clip = Clip.objects.get(id=clip_id)
    logger.debug("Archiving {} with archive.org".format(clip.url))
    try:
        ia_url, ia_captured = savepagenow.capture_or_cache(url)
        ia_memento = Memento.objects.create(url=ia_url, archive="archive.org")
        logger.debug("Created {}".format(ia_memento))
        clip.mementos.add(ia_memento)
    except Exception as e:
        logger.debug("archive.org failed")
        logger.debug(e)


@task()
def is_memento(clip_id):
    """
    Archive a clip with archive.is.
    """
    clip = Clip.objects.get(id=clip_id)
    logger.debug("Archiving {} with archive.is".format(clip.url))
    try:
        is_url = archiveis.capture(clip.url)
        is_memento = Memento.objects.create(url=is_url, archive="archive.is")
        logger.debug("Created {}".format(is_memento))
        clip.mementos.add(is_memento)
    except Exception as e:
        logger.debug("archive.is failed")
        logger.debug(e)


@task()
def wc_memento(clip_id):
    """
    Archive a clip with webcitation.
    """
    clip = Clip.objects.get(id=clip_id)
    logger.debug("Archiving {} with webcitation".format(clip.url))
    try:
        wc_url = webcitation.capture(clip.url)
        if wc_url == clip.url:
            logger.debug("Source URL returned for some reason.")
            return None
        wc_memento = Memento.objects.create(url=wc_url, archive="webcitation.org")
        logger.debug("Created {}".format(wc_memento))
        clip.mementos.add(wc_memento)
    except Exception as e:
        logger.debug("webcitation failed")
        logger.debug(e)
