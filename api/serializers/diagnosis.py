from rest_framework import serializers
from api.models.diagnosis import Diagnosis
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.patient import PatientSerializer

from api.serializers.prediction import PredictionSerializer


class DiagnosisSerializer(serializers.ModelSerializer):
    predictions = PredictionSerializer(many=True, read_only=True, source='prediction_set')
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    patient = PatientSerializer(read_only=True)
    dermatologist = DermatologistSerializer(read_only=True)
    
    
    class Meta:
        model = Diagnosis
        fields = ('id', 'image', 'body_part', 'itchy', 'date', 'extra_derm_info', 'predictions', 'patient', 'dermatologist', 'approved', 'action')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('prediction_set')
        