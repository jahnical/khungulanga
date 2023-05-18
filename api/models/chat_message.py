from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.appointment import Appointment, AppointmentSerializer
from api.models.appointment_chat import AppointmentChat, AppointmentChatSerializer

from api.models.diagnosis import Diagnosis, DiagnosisSerializer


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    chat = models.ForeignKey(AppointmentChat, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    chat = AppointmentChatSerializer()
    diagnosis = DiagnosisSerializer(allow_null=True)
    appointment = AppointmentSerializer(allow_null=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text', 'chat', 'diagnosis', 'appointment', 'date', 'time', 'seen']
