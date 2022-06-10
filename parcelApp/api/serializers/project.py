from rest_framework import serializers
from api.serializers.note import NoteOutputSerializer
from api.models import Project, Parcel, Note
from django.db.models import Count


class PostPutProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description", "color")


class ParcelGeomIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ("identifier", "geom_wkt")


class ProjectOutputSerializer(serializers.ModelSerializer):
    parcels = ParcelGeomIdentifierSerializer(many=True)

    parcels_count = serializers.SerializerMethodField()
    notes_count = serializers.SerializerMethodField()
    parcels_photos_count = serializers.SerializerMethodField()
    parcels_notes_count = serializers.SerializerMethodField()

    def get_parcels_count(self, obj):
        return obj.parcels.count()

    def get_notes_count(self, obj):
        return obj.notes.count()

    def get_parcels_photos_count(self, obj):
        parcels_set = obj.parcels.annotate(photos_count=Count("photos"))
        photos_sum = 0

        for parcel in parcels_set:
            photos_sum += parcel.photos_count

        return photos_sum

    def get_parcels_notes_count(self, obj):
        parcels_set = obj.parcels.annotate(notes_count=Count("notes"))
        notes_sum = 0

        for parcel in parcels_set:
            notes_sum += parcel.notes_count

        return notes_sum

    class Meta:
        model = Project
        fields = ("id", "title", "description", "created_at", "color", "parcels_count", "notes_count", "parcels_photos_count", "parcels_notes_count", "parcels")


class ParcelMiniSerializer(serializers.ModelSerializer):
    notes_count = serializers.SerializerMethodField()
    photos_count = serializers.SerializerMethodField()


    def get_notes_count(self, obj):
        return obj.notes.count()

    def get_photos_count(self, obj):
        return obj.photos.count()

    class Meta:
        model = Parcel
        fields = ("id", "identifier", "voivodeship", "county", "commune", "region", "parcel_num", "photos_count", "notes_count", "geom_wkt")


class GetProjectDetailsSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()
    parcels = serializers.SerializerMethodField()


    def get_notes(self, obj):
        notes = obj.notes.all().order_by("-updated_at")
        return NoteOutputSerializer(notes, many=True).data

    def get_parcels(self, obj):
        parcels = obj.parcels.all().order_by("-created_at")
        return ParcelMiniSerializer(parcels, many=True).data

    class Meta:
        model = Project
        fields = ("notes", "parcels", )






