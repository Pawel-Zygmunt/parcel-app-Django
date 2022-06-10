from rest_framework import routers
from api.views.parcel import ParcelViewSet
from api.views.project import ProjectViewSet

from django.urls import include, path


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'parcels', ParcelViewSet)

urlpatterns = [
    path("", include(router.urls))
]
