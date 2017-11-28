from django.core.management.base import BaseCommand
from archive import tasks
from archive.models import Clip


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip_list = Clip.objects.all()

        # Backload webcitation
        no_wc = [c for c in clip_list if not c.mementos.filter(archive="webcitation.org").count()]
        logger.debug("{} clips lack a webcitation memento".format(len(no_wc)))
        for c in no_wc[:25]:
            logger.debug("Backloading a webcitation URL for {}".format(c.url))
            tasks.wc_memento.delay(c.id)

        # Backload webcitation
        no_is = [c for c in clip_list if not c.mementos.filter(archive="archive.is").count()]
        logger.debug("{} clips lack an archive.is memento".format(len(no_is)))
        for c in no_is[:25]:
            logger.debug("Backloading a archive.is URL for {}".format(c.url))
            tasks.is_memento.delay(c.id)
