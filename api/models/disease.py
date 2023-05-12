from django.db import models
from rest_framework import serializers

from api.models.treatment import TreatmentSerializer

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    severity = models.IntegerField(choices=[(1, "Mild"), (2, "Moderate"), (3, "Severe")])


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