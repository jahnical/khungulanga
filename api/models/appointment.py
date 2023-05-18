from django.db import models
from rest_framework import serializers

from api.models.patient import Patient, PatientSerializer
from api.models.dermatologist import Dermatologist, DermatologistSerializer

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
    
class AppointmentSerializer(serializers.ModelSerializer):
    dermatologist = DermatologistSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'dermatologist', 'patient', 'book_date', 'appo_date', 'done', 'duration', 'cost', 'patient_approved', 'dermatologist_approved']
