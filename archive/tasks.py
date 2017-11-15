import webcitation
from celery.decorators import task
from archive.models import Memento, Clip


@task()
def wc_memento(clip_id, url):
    clip = Clip.objects.get(id=clip_id)
    url = "http://www.latimes.com/"
    print("Archiving {}".format(url))
    try:
        wc_url = webcitation.capture(url)
        wc_memento = Memento.objects.create(url=wc_url, archive="webcitation.org")
        clip.mementos.add(wc_memento)
    except Exception as e:
        print("webcitation failed")
        print(e)
    return wc_memento
