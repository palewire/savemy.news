from django.core.management.base import BaseCommand, CommandError
from archive import tasks
from archive.models import Clip, Memento


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip = Clip.objects.all()[0]
        tasks.wc_memento.delay(clip.id)
