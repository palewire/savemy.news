import webcitation
from celery.decorators import task
from archive.models import Memento, Clip


@task()
def wc_memento(clip_id):
    clip = Clip.objects.get(id=clip_id)
    print("Archiving {} with webcitation".format(clip.url))
    try:
        wc_url = webcitation.capture(clip.url)
        wc_memento = Memento.objects.create(url=wc_url, archive="webcitation.org")
        clip.mementos.add(wc_memento)
        return wc_memento
    except Exception as e:
        print("webcitation failed")
        print(e)
