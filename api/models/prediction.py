from django.db import models
from api.models.disease import DiseaseSerializer
from rest_framework import serializers

class Prediction(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, null=True)
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.CASCADE)
    probability = models.FloatField(default=0.0)

class PredictionSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer()

    class Meta:
        model = Prediction
        fields = ('disease', 'probability')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('disease')
