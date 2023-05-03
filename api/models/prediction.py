from django.db import models
from api.models.disease import Disease
from api.models.diagnosis import Diagnosis

class Prediction(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    probability = models.FloatField(default=0.0)