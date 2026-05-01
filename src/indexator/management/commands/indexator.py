from django.core.management import BaseCommand
from blake3 import blake3
from indexator.models import MediaFile



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

        path = './2026-05-01_11-36.png'

        self.stdout.write(file_hash(path))
