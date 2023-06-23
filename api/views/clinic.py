from rest_framework import generics
from api.models.clinic import Clinic
from api.serializers.clinic import ClinicSerializer

class ClinicAPIView(generics.ListCreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

class ClinicDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
