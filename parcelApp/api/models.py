from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import sys
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class ProjectNote(BaseModel):
    pass


class ParcelNote(BaseModel):
    pass


class Note(BaseModel):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f'{self.title} {self.content_type}'


class Project(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    notes = GenericRelation(Note, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.title



class Parcel(BaseModel):
    identifier = models.CharField(max_length=255, unique=True)
    voivodeship = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    parcel_num = models.CharField(max_length=255)
    geom_wkt = models.JSONField(default=list())
    created_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="parcels")
    notes = GenericRelation(Note, related_name="notes")

    def __str__(self):
        return self.identifier


class ParcelPhoto(BaseModel):
    image = models.ImageField(upload_to="images/")
    marker_image = models.ImageField(upload_to="markers/")
    active_marker_image = models.ImageField(upload_to="active_markers/")
    latitude = models.DecimalField(decimal_places=30, max_digits=32, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(decimal_places=30, max_digits=33, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name="photos")


    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     # Opening the uploaded image
    #     im = Image.open(self.image)
    #
    #     output = BytesIO()
    #
    #     original_width, original_height = im.size
    #     aspect_ratio = round(original_width / original_height)
    #     desired_height = 400  # Edit to add your desired height in pixels
    #     desired_width = desired_height * aspect_ratio
    #
    #     # Resize the image
    #     im = im.resize((desired_width, desired_height))
    #
    #
    #     # after modifications, save it to the output
    #     im.save(output, format='JPEG', quality=100)
    #     output.seek(0)
    #
    #     # change the imagefield value to be the newley modifed image value
    #     self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
    #                                       sys.getsizeof(output), None)
    #
    #     super(ParcelPhoto, self).save()
