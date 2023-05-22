from rest_framework import serializers
from api.models.appointment import Appointment

from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.patient import PatientSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    dermatologist = DermatologistSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'dermatologist', 'patient', 'book_date', 'appo_date', 'done', 'extra_info', 'duration', 'cost', 'patient_approved', 'dermatologist_approved', 'patient_rejected', 'dermatologist_rejected']
