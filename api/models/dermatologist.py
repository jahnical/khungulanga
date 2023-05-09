from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

class Dermatologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    work_email = models.EmailField()
    phone_number_1 = models.CharField(max_length=13)
    phone_number_2 = models.CharField(max_length=13)
    clinic = models.CharField(max_length=100)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    location_desc = models.CharField(max_length=100) 

class DermatologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dermatologist
        fields = ['id', 'qualification', 'work_email', 'phone_number_1', 'phone_number_2', 'clinic', 'location_lat', 'location_lon', 'location_desc']