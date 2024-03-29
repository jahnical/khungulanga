from rest_framework import serializers
from api.models.prediction import Prediction

from api.serializers.disease import DiseaseSerializer

class PredictionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Prediction model.
    """
    disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = ('id', 'disease', 'probability', 'approved', 'treatment', 'treatment_id')
        
    def get_queryset(self):
        """
        Returns the queryset for the serializer.
        """
        queryset = super().get_queryset()
        return queryset.select_related('disease')
