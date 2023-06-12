from rest_framework import serializers

from api.models.slot import Slot

class SlotSerializer(serializers.ModelSerializer):
    #dermatologist = DermatologistSerializer(read_only=True)
    
    class Meta:
        model = Slot
        fields = ['id', 'dermatologist_id', 'start_time', 'scheduled', 'day_of_week']