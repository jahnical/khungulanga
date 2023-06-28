from rest_framework import serializers
from api.models.appointment_chat import AppointmentChat
from api.serializers.appointment import AppointmentSerializer
from api.serializers.chat_message import ChatMessageSerializer
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.patient import PatientSerializer

class AppointmentChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the AppointmentChat model.
    """
    patient = PatientSerializer()
    dermatologist = DermatologistSerializer()
    appointment = AppointmentSerializer()
    messages = ChatMessageSerializer(many=True, read_only=True, source="chatmessage_set")

    class Meta:
        model = AppointmentChat
        fields = ['id', 'patient', 'dermatologist', 'appointment', 'messages']

    def get_queryset(self):
        """
        Returns the queryset for the serializer, with related chat messages.
        """
        queryset = super().get_queryset()
        return queryset.select_related('chatmessage_set')
