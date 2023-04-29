from django.db import models


class Symptom(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    