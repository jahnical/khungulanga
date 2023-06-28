from rest_framework import serializers
from api.models.appointment import Appointment
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.slot import SlotSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Appointment model.
    """
    dermatologist = DermatologistSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    diagnosis = DiagnosisSerializer(allow_null=True)
    slot = SlotSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'diagnosis', 'dermatologist', 'patient', 'book_date', 'appo_date', 'done', 'extra_info', 'duration', 'cost', 'patient_removed', 'dermatologist_removed', 'patient_cancelled', 'dermatologist_cancelled', 'slot']
