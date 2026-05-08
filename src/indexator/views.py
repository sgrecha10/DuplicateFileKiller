from django.db.models import Sum, F, Max
from django.http import HttpResponse
from django.views.generic.base import View
from indexator.models import MediaFile
import json


class IndexView(View):
    def get(self, request):
        media_file_quantity = MediaFile.objects.count()
        media_file_total_size = MediaFile.objects.aggregate(Sum('size'))['size__sum'] / (1024*1024*1024)
        media_file_black3_unique_quantity = MediaFile.objects.values('blake3').distinct().count()
        media_file_black3_unique_total_size = (
            MediaFile.objects.values('blake3').annotate(
                file_size=Max('size'),
            ).aggregate(
                total=Sum('file_size'),
            )['total'] / (1024*1024*1024)
        )

        data = {
            'MediaFile quantity:': f'{media_file_quantity}',
            'MediaFile total size:': f'{media_file_total_size:.2f} Gb.',
            'Media file black3 unique quantity:': f'{media_file_black3_unique_quantity}',
            'Media file black3 unique total size:': f'{media_file_black3_unique_total_size:.2f} Gb.',
        }

        return HttpResponse(content=json.dumps(data), content_type="application/json")
