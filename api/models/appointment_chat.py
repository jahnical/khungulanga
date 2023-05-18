from django.db import models
from api.models.appointment import Appointment, AppointmentSerializer
from api.models.patient import Patient, PatientSerializer
from api.models.diagnosis import Diagnosis, DiagnosisSerializer
from api.models.dermatologist import Dermatologist, DermatologistSerializer
from rest_framework import serializers

class AppointmentChat(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
    dermatologist = models.ForeignKey(Dermatologist, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

class AppointmentChatSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    diagnosis = DiagnosisSerializer()
    dermatologist = DermatologistSerializer()
    appointment = AppointmentSerializer()

    class Meta:
        model = AppointmentChat
        fields = ['id', 'patient', 'diagnosis', 'dermatologist', 'appointment']
