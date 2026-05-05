from django.db import models


class MediaFile(models.Model):
    path = models.TextField(
        verbose_name='Path',
        unique=True,
    )
    size = models.PositiveBigIntegerField(
        verbose_name='Size',
    )
    file_type = models.TextField(
        verbose_name='File type',
    )
    mtime = models.DateTimeField(
        verbose_name='mtime',
    )
    blake3 = models.TextField(
        verbose_name='BLAKE3',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created',
    )

    class Meta:
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'

    def __str__(self):
        return self.path
