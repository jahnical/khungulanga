from django.db import models


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    severity = models.IntegerField(choices=[(1, "Mild"), (2, "Moderate"), (3, "Severe")])