from django.db import models
from api.models.patient import Patient
class Diagnosis(models.Model):
    image = models.ImageField(upload_to='media/diagnosis/%Y/%m/%d/')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    body_part = models.CharField(max_length=100)
    itchy = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
