from django.contrib import admin
from .models import CopiedFile
from django.db import models
from django.forms import Textarea


@admin.register(CopiedFile)
class CopiedFileAdmin(admin.ModelAdmin):
    list_display = (
        'blake3',
        'path',
        'created',
    )

    readonly_fields = list_display

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 80})},
    }
