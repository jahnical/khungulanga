from django.db import models
from api.models.appointment import Appointment
from api.models.patient import Patient
from api.models.diagnosis import Diagnosis
from api.models.dermatologist import Dermatologist

class AppointmentChat(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    dermatologist = models.ForeignKey(Dermatologist, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)