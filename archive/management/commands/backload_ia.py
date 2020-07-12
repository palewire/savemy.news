from django.core.management.base import BaseCommand
import time
import logging
from archive import tasks
from archive.models import Clip
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip_list = Clip.objects.all().order_by("?")
        no_ia = [c for c in clip_list if not c.mementos.filter(archive="archive.org").count()]
        logger.debug("{} clips lack an archive.org memento".format(len(no_ia)))
        for c in no_ia[:8]:
            logger.debug("Backloading archive.org URL for {}".format(c.url))
            tasks.ia_memento.delay(c.id)
            time.sleep(5)
