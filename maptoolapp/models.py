from django.db import models


# Create your models here.


class Locations(models.Model):
    itemgroup = models.ForeignKey('ItemGroup')
    locality = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    generated_longitude = models.CharField(max_length=50)
    generated_latitude = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    datetime = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    mapurl = models.CharField(max_length=200)

class Urls(models.Model):
    itemgroup = models.ForeignKey('ItemGroup')
    url_1 = models.CharField(max_length=200)
    description_1 = models.CharField(max_length=50)
    url_2 = models.CharField(max_length=200)
    description_2 = models.CharField(max_length=50)
    url_3 = models.CharField(max_length=200)
    description_3 = models.CharField(max_length=50)

class ItemGroup(models.Model):
    context_id = models.CharField(max_length=50)
    resource_link_id = models.CharField(max_length=50)
    custom_canvas_course_id = models.CharField(max_length=50)
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=500)