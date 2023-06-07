from rest_framework import serializers

from api.models.treatment import Treatment


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ('title', 'description')