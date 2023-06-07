from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.appointment import Appointment

from api.models.appointment_chat import AppointmentChat
from api.models.patient import Patient
from api.serializers.appointment_chat import AppointmentChatSerializer
from api.models.dermatologist import Dermatologist

class AppointmentChatView(APIView):
    def get(self, request):
        print(request.user)
        is_patient = Patient.objects.all().filter(user=request.user).count() > 0
        appointment_chats = AppointmentChat.objects.all().filter(patient_id=request.user.patient.id) if is_patient else AppointmentChat.objects.all().filter(dermatologist_id=request.user.dermatologist.id) 
        print(request.user, is_patient, appointment_chats) 
        serializer = AppointmentChatSerializer(appointment_chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            data = {**request.data}
            data.pop('id')
            data.pop('diagnosis_id')
            try:
                appointment_chat = AppointmentChat.objects.get(dermatologist_id=data['dermatologist_id'], patient_id=data['patient_id'])
                return Response(AppointmentChatSerializer(appointment_chat).data, status=status.HTTP_200_OK)
            except AppointmentChat.DoesNotExist:
                appointment = Appointment.objects.create(**{'patient_id': data['patient_id'], 'dermatologist_id': data['dermatologist_id']})
                appointment.save()
                data['appointment_id'] = appointment.id
                chat = AppointmentChat.objects.create(**data)
                chat.save()
                return Response(AppointmentChatSerializer(chat).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentChatDetail(APIView):
    def get_object(self, pk):
        try:
            return AppointmentChat.objects.get(pk=pk)
        except AppointmentChat.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        appointment_chat = self.get_object(pk)
        serializer = AppointmentChatSerializer(appointment_chat)
        return Response(serializer.data)

    def put(self, request, pk):
        appointment_chat = self.get_object(pk)
        serializer = AppointmentChatSerializer(appointment_chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment_chat = self.get_object(pk)
        appointment_chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
