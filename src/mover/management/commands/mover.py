from datetime import datetime
from pathlib import Path

from blake3 import blake3
from django.conf import settings
from django.core.management import BaseCommand
from time import sleep

from indexator.models import MediaFile
from mover.models import CopiedFile


class Command(BaseCommand):
    help = 'Копирование проиндексированных файлов'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start...'))

        if not settings.TARGET_DIR:
            self.stdout.write(self.style.ERROR('TARGET_DIR not set.'))
            return

        media_file_qs = MediaFile.objects.all().order_by('id')
        pointer_id = 0
        chunk_size = 500

        while chunk := media_file_qs.filter(id__gt=pointer_id)[:chunk_size]:
            self.stdout.write(str(pointer_id))

            for media_file in chunk:
                pointer_id = media_file.id
                try:
                    copied_file = CopiedFile.objects.create(blake3=media_file.blake3)
                except Exception as e:
                    self.stdout.write(self.style.NOTICE(str(e)))
                    continue

                # тут надо копировать файл
                # copied_file.path = ...
                # copied_file.save(update_fields=['path'])

            # sleep(1)

        self.stdout.write(self.style.SUCCESS('End.'))
