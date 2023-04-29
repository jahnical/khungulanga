from django.contrib.auth.models import User
from django.db import models


class Dermatologist(User):
    qualification = models.CharField(max_length=100)
    work_email = models.EmailField()
    phone_number_1 = models.CharField(max_length=13)
    phone_number_2 = models.CharField(max_length=13)
    clinic = models.CharField(max_length=100)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    location_desc = models.CharField(max_length=100)