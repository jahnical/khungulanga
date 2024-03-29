from rest_framework import serializers
from api.models.dermatologist import Dermatologist
from api.serializers.clinic import ClinicSerializer
from api.serializers.slot import SlotSerializer
from api.serializers.user import UserSerializer


class DermatologistSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dermatologist model.
    """
    user = UserSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)
    slots = SlotSerializer(many=True, read_only=True, source="slot_set")

    class Meta:
        model = Dermatologist
        fields = ['id', 'status', 'slots', 'qualification', 'email', 'phone_number', 'clinic', 'user', 'hourly_rate', 'specialization']
    
    def get_queryset(self):
        """
        Custom method to optimize queryset by selecting related models.
        """
        queryset = super().get_queryset().select_related('slot_set')
        return queryset.select_related('user')
