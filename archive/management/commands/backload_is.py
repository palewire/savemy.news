from django.core.management.base import BaseCommand
import logging
from archive import tasks
from archive.models import Clip
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip_list = Clip.objects.all().order_by("?")

        no_is = [c for c in clip_list if not c.mementos.filter(archive="archive.is").count()]
        logger.debug("{} clips lack an archive.is memento".format(len(no_is)))
        for c in no_is[:5]:
            logger.debug("Backloading archive.is URL for {}".format(c.url))
            tasks.is_memento.delay(c.id)
