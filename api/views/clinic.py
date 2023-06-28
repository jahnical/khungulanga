from rest_framework import generics
from api.models.clinic import Clinic
from api.serializers.clinic import ClinicSerializer

class ClinicAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating clinics.
    """
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

class ClinicDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting individual clinics.
    """
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
