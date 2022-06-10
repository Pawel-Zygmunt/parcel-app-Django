from django.http import HttpResponseNotFound
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Parcel, Project, ParcelPhoto
from api.serializers.parcel import PutParcelSerializer, PostParcelSerializer, ParcelDetailsSerializer, ParcelOutputSerializer, UploadParcelPhotoSerializer, ParcelPhotoSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_classes = {
        'create': PostParcelSerializer,
        'update': PutParcelSerializer,
        'retrieve': ParcelDetailsSerializer
    }
    default_serializer_class = ParcelOutputSerializer
    pagination_class = None
    http_method_names = ['get', "post", "delete", "put"]
    lookup_field = "identifier"

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @swagger_auto_schema(responses={201: ParcelOutputSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = PostParcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # project_instance = Project.objects.only("id").get(id=serializer.validated_data['project'])
        #
        # new_parcel = dict(serializer.data)
        # del new_parcel['project']

        parcel = Parcel.objects.create(**serializer.validated_data)
        serialized = ParcelOutputSerializer(parcel, many=False)
        return Response(serialized.data, status=201)

    @swagger_auto_schema(responses={200: ParcelOutputSerializer()})
    def update(self, request, *args, **kwargs):
        serializer = PutParcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parcel = self.get_object()
        parcel.project = serializer.validated_data['project']
        parcel.save()
        serialized = ParcelOutputSerializer(parcel, many=False)
        return Response(serialized.data, status=200)

    @swagger_auto_schema(request_body=UploadParcelPhotoSerializer)
    @action(detail=True, methods=["post"])
    def upload_photo(self, request, *args, **kwargs):
        serializer = UploadParcelPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parcel = self.get_object()
        photo = ParcelPhoto.objects.create(parcel=parcel, **serializer.validated_data)

        serialized = ParcelPhotoSerializer(photo, many=False, context={'request': request})

        return Response(serialized.data, status=200)

    @swagger_auto_schema(tags=["parcels"])
    @action(detail=False, methods=["get"], url_path='get_by_lat_lng/(?P<latitude>[^/]+)/(?P<longitude>[^/]+)')
    def get_by_lat_lng(self, request, *args, **kwargs):
        point = Feature(geometry=Point((float(kwargs['latitude']), float(kwargs['longitude']))))
        found_parcel = None

        for parcel in Parcel.objects.all():
            transformed_geom_wkt = list(map(lambda x: (float(x.split(",")[0]),  float(x.split(",")[1])), parcel.geom_wkt))
            polygon = Polygon([transformed_geom_wkt])

            if boolean_point_in_polygon(point, polygon):
                found_parcel = parcel
                break

        if found_parcel is None:
            return HttpResponseNotFound()

        serialized = ParcelDetailsSerializer(found_parcel, many=False, context={'request': request})
        return Response(serialized.data, status=200)


