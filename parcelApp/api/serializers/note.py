from rest_framework import serializers
from api.models import Note


class PostPutNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("title", "content")


class NoteOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "title", "content", "created_at", "updated_at")
