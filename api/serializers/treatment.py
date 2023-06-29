from rest_framework import serializers
from api.models.treatment import Treatment

class TreatmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Treatment model.
    """
    class Meta:
        model = Treatment
        fields = ('title', 'description', 'id')
