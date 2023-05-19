from rest_framework import serializers

from api.models.disease import Disease
from api.serializers.treatment import TreatmentSerializer

class DiseaseSerializer(serializers.ModelSerializer):
    treatments = TreatmentSerializer(many=True, read_only=True, source='treatment_set')

    class Meta:
        model = Disease
        fields = ('id', 'name', 'description', 'severity', 'treatments')
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('treatment_set')
    
    def get_severity_display(self, obj):
        return obj.get_severity_display()
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['severity'] = self.get_severity_display(instance)
        return ret