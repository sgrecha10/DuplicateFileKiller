from django.contrib import admin
from .models import MediaFile
from django.db import models
from django.forms import Textarea
from django.forms.widgets import Input


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'path',
        'size',
        'file_type',
        'mtime',
        'blake3',
        # 'updated',
        # 'created',
    )

    readonly_fields = list_display

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 80})},
    }