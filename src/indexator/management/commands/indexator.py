from datetime import datetime
from pathlib import Path

from blake3 import blake3
from django.conf import settings
from django.core.management import BaseCommand

from indexator.models import MediaFile
from django.db import IntegrityError


def file_hash(path: str) -> str:
    h = blake3()

    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)

    return h.hexdigest()


class Command(BaseCommand):
    help = 'Индексация медиа файлов'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start...'))

        for path in Path(settings.SOURCE_DIR).rglob("*"):
            if path.is_file():
                file_type = path.suffix

                if file_type not in settings.ALLOWED_SUFFIXES:
                    continue

                try:
                    MediaFile.objects.create(
                        path=str(path),
                        size= path.stat().st_size,
                        file_type= file_type,
                        mtime= datetime.fromtimestamp(
                            path.stat().st_mtime
                        ),
                        blake3= file_hash(str(path)),
                    )
                    self.stdout.write(self.style.SUCCESS(str(path)))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(str(e)))

        self.stdout.write(self.style.SUCCESS('End.'))
