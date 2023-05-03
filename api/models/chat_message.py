from django.db import models
from django.contrib.auth.models import User
from api.models.appointment import Appointment
from api.models.appointment_chat import AppointmentChat

from api.models.diagnosis import Diagnosis


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    chat = models.ForeignKey(AppointmentChat, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)