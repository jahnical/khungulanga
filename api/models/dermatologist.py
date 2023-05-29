from django.contrib.auth.models import User
from django.db import models

class Dermatologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=13)
    clinic = models.CharField(max_length=200)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    location_desc = models.CharField(max_length=100)
    