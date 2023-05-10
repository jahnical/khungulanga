from django.db import models
from api.models.patient import Patient
from api.models.disease import Disease
from rest_framework import serializers

from api.models.prediction import PredictionSerializer

class Diagnosis(models.Model):
    image = models.ImageField(upload_to='media/diagnosis/%Y/%m/%d/')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    body_part = models.CharField(max_length=100)
    itchy = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    


class DiagnosisSerializer(serializers.ModelSerializer):
    predictions = PredictionSerializer(many=True, read_only=True, source='prediction_set')
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Diagnosis
        fields = ('id', 'image', 'body_part', 'itchy', 'date', 'predictions')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('prediction_set')
        
