from django.db import models


# Create your models here.


class Locations(models.Model):
    user_id = models.CharField(max_length=50)
    resource_link_id = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    generated_longitude = models.CharField(max_length=50)
    generated_latitude = models.CharField(max_length=50)
    context_id = models.CharField(max_length=50)
    custom_canvas_course_id = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    datetime = models.CharField(max_length=50)

    first_name = models.CharField(max_length=50)
    first_name_permission = models.BooleanField(default=False)
    last_name = models.CharField(max_length=50)
    last_name_permission = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=250)
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    mapurl = models.CharField(max_length=200)
