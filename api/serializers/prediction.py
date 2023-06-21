from rest_framework import serializers
from api.models.prediction import Prediction

from api.serializers.disease import DiseaseSerializer

class PredictionSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = ('id', 'disease', 'probability', 'approved', 'treatment')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('disease')
