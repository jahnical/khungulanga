from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.chat_message import ChatMessage
from api.serializers.appointment import AppointmentSerializer

from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.user import UserSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    diagnosis = DiagnosisSerializer(allow_null=True)
    appointment = AppointmentSerializer(allow_null=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text', 'chat_id', 'diagnosis', 'appointment', 'time', 'seen']
