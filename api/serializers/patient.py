from rest_framework import serializers
from api.models.patient import Patient

from api.serializers.user import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model.
    """
    user = UserSerializer(read_only=True)
    dob = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Patient
        fields = ['id', 'dob', 'gender', 'user']
    
    def get_queryset(self):
        """
        Returns the queryset for the serializer.
        """
        queryset = super().get_queryset()
        return queryset.select_related('user')
    
    def get_gender_display(self, obj):
        """
        Returns the display value of the gender field.
        """
        return obj.get_gender_display()
    
    def to_representation(self, instance):
        """
        Converts the instance to a representation dictionary.
        """
        ret = super().to_representation(instance)
        ret['gender'] = self.get_gender_display(instance)
        return ret
