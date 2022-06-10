import os

from django.contrib import admin
from .models import Parcel, Project, Note, ParcelPhoto
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe
from django.conf import settings


class ParcelPhotoInline(admin.TabularInline):
    model = ParcelPhoto
    readonly_fields = ('image_preview', )

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            #path = os.path.join(settings.Me, obj.image.url)
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ["id", "identifier"]
    inlines = [
        ParcelPhotoInline
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    pass


admin.site.register(Note)

