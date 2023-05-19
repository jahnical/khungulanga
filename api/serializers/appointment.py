from rest_framework import serializers
from api.models.appointment import Appointment

from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.patient import PatientSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    dermatologist = DermatologistSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'dermatologist', 'patient', 'book_date', 'appo_date', 'done', 'duration', 'cost', 'patient_approved', 'dermatologist_approved']
