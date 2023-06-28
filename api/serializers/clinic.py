from rest_framework import serializers
from api.models.clinic import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    """
    Serializer for the Clinic model.
    """
    class Meta:
        model = Clinic
        fields = '__all__'
