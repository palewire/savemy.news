from django.core.management.base import BaseCommand, CommandError
from archive import tasks
from archive.models import Clip, Memento


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip_list = Clip.objects.all()
        no_wc = [c for c in clip_list if not c.mementos.filter(archive="webcitation.org").count()]
        for c in no_wc[:10]:
            tasks.wc_memento.delay(clip.id)
