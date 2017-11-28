from django.core.management.base import BaseCommand
import logging
from archive import tasks
from archive.models import Clip
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip_list = Clip.objects.all()

        # Backload webcitation
        no_wc = [c for c in clip_list if not c.mementos.filter(archive="webcitation.org").count()]
        logger.debug("{} clips lack a webcitation memento".format(len(no_wc)))
        for c in no_wc[:25]:
            logger.debug("Backloading webcitation URL for {}".format(c.url))
            tasks.wc_memento.delay(c.id)
