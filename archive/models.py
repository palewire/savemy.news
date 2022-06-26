from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Memento(models.Model):
    timestamp = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
    )
    ARCHIVE_CHOICES = (
        ('archive.org', 'archive.org'),
        ('archive.is', 'archive.is'),
        ('webcitation.org', 'webcitation.org'),
    )
    archive = models.CharField(
        max_length=1000,
        choices=ARCHIVE_CHOICES,
        db_index=True,
        default=ARCHIVE_CHOICES[0][0],
    )
    url = models.URLField(max_length=1000)

    class Meta:
        ordering = ("-timestamp",)
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.url


class Clip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=1000)
    mementos = models.ManyToManyField(Memento)

    def __str__(self):
        return self.url

    @property
    def timestamp(self):
        try:
            return self.mementos.get(archive="archive.org").timestamp
        except ObjectDoesNotExist:
            try:
                return self.mementos.latest().timestamp
            except ObjectDoesNotExist:
                return None
        except Memento.MultipleObjectsReturned:
            return self.mementos.filter(archive="archive.org")[0].timestamp

    @property
    def memento_count(self):
        return self.mementos.count()

    @property
    def ia_memento(self):
        try:
            return self.mementos.get(archive="archive.org")
        except ObjectDoesNotExist:
            return None
        except Memento.MultipleObjectsReturned:
            return self.mementos.filter(archive="archive.org")[0].timestamp
