import os
import shutil
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.management import BaseCommand

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
                    # self.stdout.write(self.style.NOTICE(str(e)))
                    continue

                # тут надо копировать файл
                if target_path := self._copy_file(media_file):
                    copied_file.path = target_path
                    copied_file.save(update_fields=['path'])

            # sleep(1)

        self.stdout.write(self.style.SUCCESS('End.'))

    def _copy_file(self, media_file: MediaFile) -> Optional[str]:
        try:
            mtime = media_file.mtime
            year_dir_name = mtime.year
            month_dir_name = mtime.month
            file_name = media_file.path.split('/')[-1]
            target_path = f'{settings.TARGET_DIR}/{year_dir_name}/{month_dir_name:02}/{file_name}'

            src = Path(str(media_file.path))
            dst = Path(target_path)

            # создать директории
            dst.parent.mkdir(parents=True, exist_ok=True)

            # копировать файл
            shutil.copy2(src, dst)

            # нормализация прав
            os.chmod(dst, 0o644)

        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return ''

        return target_path
