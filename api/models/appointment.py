from django.db import models

from api.models.patient import Patient
from api.models.dermatologist import Dermatologist

class Appointment(models.Model):
    dermatologist = models.ForeignKey(Dermatologist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    book_date = models.DateField(null=True)
    appo_date = models.DateField(null=True)
    done = models.BooleanField(default=False)
    duration = models.DurationField(null=True)
    cost = models.FloatField(default=0.0)
    patient_approved = models.DateTimeField(null=True)
    dermatologist_approved = models.DateTimeField(null=True)
    patient_rejected = models.DateTimeField(null=True)
    dermatologist_rejected = models.DateTimeField(null=True)