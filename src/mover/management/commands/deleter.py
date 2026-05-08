from pathlib import Path

from django.core.management import BaseCommand

from indexator.models import MediaFile
from mover.models import CopiedFile


class Command(BaseCommand):
    """Умное удаление. Удаление исходников скопированных файлов.

    Перед удалением проверяем, что для удаляемого файла есть запись в CopiedFile,
    если нет записи - пропускаем.
    """
    help = 'Удаление исходников скопированных файлов'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start...'))

        media_file_qs = MediaFile.objects.all().order_by('id')
        pointer_id = 0
        chunk_size = 500

        while chunk := media_file_qs.filter(id__gt=pointer_id)[:chunk_size]:
            self.stdout.write(str(pointer_id))

            for media_file in chunk:
                pointer_id = media_file.id

                is_exists = CopiedFile.objects.filter(
                    blake3=media_file.blake3,
                    size=media_file.size,
                    mtime=media_file.mtime,
                    path__isnull=False,
                ).exclude(
                    path='',
                ).exists()

                if is_exists:
                    # Можно удалять.
                    Path(media_file.path).unlink(missing_ok=True)
                    MediaFile.objects.filter(pk=media_file.id).delete()

        self.stdout.write(self.style.SUCCESS('End.'))
