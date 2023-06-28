from rest_framework import serializers
from api.models.disease import Disease
from api.serializers.treatment import TreatmentSerializer


class DiseaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Disease model.
    """
    treatments = TreatmentSerializer(many=True, read_only=True, source='treatment_set')

    class Meta:
        model = Disease
        fields = ('id', 'name', 'description', 'severity', 'treatments')
        
    def get_queryset(self):
        """
        Custom method to optimize queryset by selecting related models.
        """
        queryset = super().get_queryset()
        return queryset.select_related('treatment_set')
    
    def get_severity_display(self, obj):
        """
        Method to retrieve the display value for the 'severity' field.
        """
        return obj.get_severity_display()
    
    def to_representation(self, instance):
        """
        Method to customize the serialized representation of the instance.
        """
        ret = super().to_representation(instance)
        ret['severity'] = self.get_severity_display(instance)
        return ret
