from django.core.management.base import BaseCommand, CommandError
import webcitation
from archive.models import Clip, Memento


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = "http://www.latimes.com/"
        print("Archiving {}".format(url))
        try:
            wc_url = webcitation.capture(url)
            wc_memento = Memento.objects.create(url=wc_url, archive="webcitation.org")
        except Exception as e:
            print("webcitation failed")
            print(e)
