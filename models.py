from django.db import models


# Create your models here.


class Locations(models.Model):
    course_id = models.IntegerField()
    user_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    first_name_permission = models.BooleanField()
    last_name_permission = models.BooleanField()
    email_permission = models.BooleanField()
    organization_permission = models.BooleanField()
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    mapurl = models.CharField(max_length=200)
    generated_latitude = models.CharField(max_length=50)
    generated_longitude = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    method = models.CharField(max_length=10)

    class Meta:
        unique_together = (("course_id", "user_id"),)
