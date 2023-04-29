from django.db import models
from api.models.symptom import Symptom


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    symptoms = models.ManyToManyField(Symptom)
    