from rest_framework import serializers
from api.models.dermatologist import Dermatologist

from api.serializers.user import UserSerializer


class DermatologistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Dermatologist
        fields = ['id', 'qualification', 'work_email', 'phone_number_1', 'phone_number_2', 'clinic', 'location_lat', 'location_lon', 'location_desc', 'user']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('user')