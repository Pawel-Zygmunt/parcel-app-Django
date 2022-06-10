from rest_framework import serializers
from api.models import Parcel, ParcelPhoto, Project
from api.serializers.note import NoteOutputSerializer
import base64


class PostParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ("identifier", "voivodeship", "county", "commune", "region", "parcel_num", "geom_wkt", "project")


class PutParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ("project",)


class UploadParcelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelPhoto
        fields = ("image", "latitude", "longitude", "marker_image", "active_marker_image")


class ParcelOutputSerializer(serializers.ModelSerializer):
    projectId = serializers.IntegerField(source="project.id")
    projectTitle = serializers.CharField(source="project.title")
    projectColor = serializers.CharField(source="project.color")

    class Meta:
        model = Parcel
        fields = ("id", "identifier", "voivodeship", "county", "commune",
                  "region", "parcel_num", "geom_wkt", "projectId", "projectTitle", "projectColor")


class ParcelPhotoSerializer(serializers.ModelSerializer):
    marker_image = serializers.SerializerMethodField(read_only=True)
    active_marker_image = serializers.SerializerMethodField(read_only=True)

    def get_marker_image(self, obj):
        img = open(obj.marker_image.path, "rb")
        data = img.read()
        return base64.b64encode(data)

    def get_active_marker_image(self, obj):
        img = open(obj.active_marker_image.path, "rb")
        data = img.read()
        return base64.b64encode(data)

    class Meta:
        model = ParcelPhoto
        fields = ("image", "marker_image", "active_marker_image", "latitude", "longitude",)


class ParcelDetailsSerializer(serializers.ModelSerializer):
    notes = NoteOutputSerializer(many=True)
    photos = ParcelPhotoSerializer(many=True)
    projectId = serializers.IntegerField(source="project.id")
    projectTitle = serializers.CharField(source="project.title")
    projectColor = serializers.CharField(source="project.color")

    class Meta:
        model = Parcel
        fields = ("id", "identifier", "voivodeship", "county", "commune",
                  "region", "parcel_num", "geom_wkt", "notes", "photos", "projectTitle", "projectId", "projectColor")






