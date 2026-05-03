from datetime import datetime
from pathlib import Path

from blake3 import blake3
from django.core.management import BaseCommand

from indexator.models import MediaFile

BASE_DIR = '/home/grechnev/Изображения'

ALLOWED_SUFFIXES = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
]


def file_hash(path: str) -> str:
    h = blake3()

    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)

    return h.hexdigest()


class Command(BaseCommand):
    help = 'Индексация медиа файлов'

    # def add_arguments(self, parser):
    #     parser.add_argument('kladr_id', type=int)

    def handle(self, *args, **options):
        # kladr_id = options['kladr_id']

        self.stdout.write(self.style.NOTICE('Start...'))

        for path in Path(BASE_DIR).rglob("*"):
            if path.is_file():
                file_type = path.suffix

                if file_type not in ALLOWED_SUFFIXES:
                    continue

                self.stdout.write(str(path))

                MediaFile.objects.update_or_create(
                    path=str(path),
                    # blake3=file_hash(str(path)),
                    defaults={
                        'size': path.stat().st_size,
                        'file_type': file_type,
                        'mtime': datetime.fromtimestamp(
                            path.stat().st_mtime
                        ),
                        'blake3': file_hash(str(path)),
                    }
                )
