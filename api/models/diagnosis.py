from django.db import models
from api.models.patient import Patient
from api.models.disease import Disease

class Diagnosis(models.Model):
    image = models.ImageField(upload_to='diagnosis/%Y/%m/%d/')
    diseases = models.ManyToManyField(Disease, through='Prediction')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    body_part = models.CharField(max_length=100)
    itchy = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)