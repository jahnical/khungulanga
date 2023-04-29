from django.db import models
from api.models.patient import Patient
from api.models.disease import Disease

class Diagnosis(models.Model):
    image = models.ImageField(upload_to='diagnosis/%Y/%m/%d/')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()