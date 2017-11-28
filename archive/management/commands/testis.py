from django.core.management.base import BaseCommand
from archive import tasks
from archive.models import Clip


class Command(BaseCommand):

    def handle(self, *args, **options):
        clip = Clip.objects.all()[0]
        tasks.is_memento(clip.id)
