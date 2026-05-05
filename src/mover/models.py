from django.db import models


class CopiedFile(models.Model):
    blake3 = models.TextField(
        verbose_name='BLAKE3',
        primary_key=True,
    )
    path = models.TextField(
        verbose_name='Path',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created',
    )

    class Meta:
        verbose_name = 'Скопированный файл'
        verbose_name_plural = 'Скопированные файлы'

    def __str__(self):
        return self.path
