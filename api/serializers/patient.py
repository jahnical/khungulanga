from rest_framework import serializers
from api.models.patient import Patient

from api.serializers.user import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    dob = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Patient
        fields = ['id', 'dob', 'gender', 'user']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('user')
    
    def get_gender_display(self, obj):
        return obj.get_gender_display()
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['gender'] = self.get_gender_display(instance)
        return ret