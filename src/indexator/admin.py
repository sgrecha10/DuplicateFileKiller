from django.contrib import admin
from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'path',
        'size',
        'file_type',
        'mtime',
        'blake3',
        'updated',
        'created',
    )
