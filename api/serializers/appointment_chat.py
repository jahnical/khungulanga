from rest_framework import serializers
from api.models.appointment_chat import AppointmentChat
from api.serializers.appointment import AppointmentSerializer
from api.serializers.chat_message import ChatMessageSerializer
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer

from api.serializers.patient import PatientSerializer

class AppointmentChatSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    diagnosis = DiagnosisSerializer()
    dermatologist = DermatologistSerializer()
    appointment = AppointmentSerializer()
    messages = ChatMessageSerializer(many=True, read_only=True, source="chatmessage_set")

    class Meta:
        model = AppointmentChat
        fields = ['id', 'patient', 'diagnosis', 'dermatologist', 'appointment', 'messages']
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('chatmessage_set')