from django.db import models
from rest_framework import serializers

class Treatment(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
    description = models.TextField(max_length=500)
    title = models.CharField(max_length=100)
    

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ('title', 'description', 'min_age', 'max_age', 'gender')