from rest_framework import serializers
from api.models.diagnosis import Diagnosis

from api.serializers.prediction import PredictionSerializer


class DiagnosisSerializer(serializers.ModelSerializer):
    predictions = PredictionSerializer(many=True, read_only=True, source='prediction_set')
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Diagnosis
        fields = ('id', 'image', 'body_part', 'itchy', 'date', 'predictions')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('prediction_set')
        