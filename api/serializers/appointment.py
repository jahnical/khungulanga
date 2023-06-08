from rest_framework import serializers
from api.models.appointment import Appointment

from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.patient import PatientSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    dermatologist = DermatologistSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    diagnosis = DiagnosisSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'diagnosis', 'dermatologist', 'patient', 'book_date', 'appo_date', 'done', 'extra_info', 'duration', 'cost', 'patient_approved', 'dermatologist_approved', 'patient_rejected', 'dermatologist_rejected']
