from django.db import models
from api.models.diagnosis import Diagnosis

from api.models.patient import Patient
from api.models.dermatologist import Dermatologist
from api.models.slot import Slot

class Appointment(models.Model):
    dermatologist = models.ForeignKey(Dermatologist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    book_date = models.DateField(null=True)
    appo_date = models.DateTimeField(null=True)
    done = models.BooleanField(default=False)
    duration = models.IntegerField(null=True)
    cost = models.FloatField(default=0.0)
    extra_info = models.TextField(max_length=1000, null=True)
    patient_approved = models.DateTimeField(null=True)
    dermatologist_approved = models.DateTimeField(null=True)
    patient_rejected = models.DateTimeField(null=True)
    dermatologist_rejected = models.DateTimeField(null=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)