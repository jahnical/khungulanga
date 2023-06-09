from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.appointment import Appointment
from api.models.diagnosis import Diagnosis
from api.serializers.appointment import AppointmentSerializer
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.patient import PatientSerializer

class AppointmentView(APIView):
    def get(self, request):
        appointments = Appointment.objects.exclude(
            patient_approved=None).exclude(
                dermatologist_approved=None).filter(
            done= True if request.GET.get('done', False) == 'true' else False)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Implement other methods such as PUT, DELETE, etc.
    # Example:
    def put(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        request.data['patient'] = PatientSerializer(appointment.patient).data
        request.data['patient']['gender'] = {"Male": "M",  "Female": "F", "Other": "O"}[request.data['patient']['gender']]
        request.data['dermatologist'] = DermatologistSerializer(appointment.dermatologist).data
        app_id = request.data['diagnosis_id'] if request.data['diagnosis_id'] else appointment.diagnosis.id
        request.data['diagnosis'] = DiagnosisSerializer(Diagnosis.objects.get(pk=app_id)).data if app_id else None
        serializer = AppointmentSerializer(appointment, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
