from api.models import Project, Note, ProjectNote
from rest_framework import viewsets
from api.serializers.project import ProjectOutputSerializer, GetProjectDetailsSerializer, PostPutProjectSerializer
from api.serializers.note import PostPutNoteSerializer, NoteOutputSerializer
from rest_framework.response import Response
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import time


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_classes = {
        'retrieve': GetProjectDetailsSerializer,
        'create': PostPutProjectSerializer,
        'update': PostPutProjectSerializer,
        'list': ProjectOutputSerializer
    }
    default_serializer_class = ProjectOutputSerializer
    pagination_class = None
    http_method_names = ['get', "post", "delete", "put"]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    # def list(self, request, *args, **kwargs):
    #     projects = Project.objects.annotate(parcels_count=Count('parcels')).order_by("-created_at")
    #     serialized = ProjectOutputSerializer(projects, many=True)
    #     return Response(serialized.data)

    @swagger_auto_schema(responses={200: ProjectOutputSerializer()})
    def update(self, request, *args, **kwargs):
        serializer = PostPutProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = self.get_object()
        project.parcels_count = project.parcels.count()
        for k, v in serializer.validated_data.items():
            setattr(project, k, v)
        project.save()

        serialized = ProjectOutputSerializer(project, many=False)
        return Response(serialized.data, status=200)

    @swagger_auto_schema(responses={201: ProjectOutputSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = PostPutProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = Project.objects.create(**serializer.validated_data)
        project.parcels_count = 0
        serialized = ProjectOutputSerializer(project, many=False)
        return Response(serialized.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = GetProjectDetailsSerializer(project)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=PostPutNoteSerializer, method="POST", responses={200: NoteOutputSerializer()})
    @action(detail=True, methods=["POST"], url_path="note")
    def add_note(self, request, *args, **kwargs):
        serializer = PostPutNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = self.get_object()
        note = project.notes.create(content_type=ProjectNote, **serializer.validated_data)
        serialized = NoteOutputSerializer(note)
        return Response(serialized.data, status=201)

    @swagger_auto_schema(request_body=PostPutNoteSerializer, method="put", responses={200: NoteOutputSerializer()})
    @action(detail=True, methods=["PUT", "DELETE"], url_path="note/(?P<note_id>\w+)")
    def update_delete_note_dispatcher(self, request, *args, **kwargs):
        if request.method == "PUT":
            return self.update_note(request, *args, **kwargs)
        if request.method == "DELETE":
            return self.delete_note(request, *args, **kwargs)

        return Response(status=405)

    def update_note(self, request, *args, **kwargs):
        serializer = PostPutNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = self.get_object()
        note = get_object_or_404(project.notes, pk=kwargs.get("note_id"))

        for k, v in serializer.validated_data.items():
            setattr(note, k, v)

        note.save()
        serialized = NoteOutputSerializer(note)
        return Response(serialized.data, status=200)

    def delete_note(self, request, *args, **kwargs):
        project = self.get_object()
        note = get_object_or_404(project.notes, pk=kwargs.get("note_id"))
        note.delete()
        return Response(status=200)
