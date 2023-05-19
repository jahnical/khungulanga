from rest_framework import serializers
from api.models.prediction import Prediction

from api.serializers.disease import DiseaseSerializer

class PredictionSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer()

    class Meta:
        model = Prediction
        fields = ('disease', 'probability')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('disease')
