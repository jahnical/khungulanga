
from rest_framework import serializers
from api.models.clinic import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'