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
    """
    API view for managing appointment chats.
    """

    def get(self, request):
        """
        Get a list of appointment chats.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: The response containing the serialized appointment chats.

        """
        is_patient = Patient.objects.filter(user=request.user).exists()
        if is_patient:
            appointment_chats = AppointmentChat.objects.filter(patient_id=request.user.patient.id)
        else:
            appointment_chats = AppointmentChat.objects.filter(dermatologist_id=request.user.dermatologist.id)

        serializer = AppointmentChatSerializer(appointment_chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new appointment chat.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: The response containing the serialized appointment chat.

        """
        try:
            data = {**request.data}
            data.pop('id')
            data.pop('diagnosis_id')

            try:
                appointment_chat = AppointmentChat.objects.get(
                    dermatologist_id=data['dermatologist_id'],
                    patient_id=data['patient_id']
                )
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
    """
    API view for managing individual appointment chats.
    """

    def get_object(self, pk):
        """
        Get the appointment chat object with the specified ID.

        Args:
            pk (int): The ID of the appointment chat.

        Returns:
            api.models.appointment_chat.AppointmentChat: The appointment chat object.

        Raises:
            Http404: If the appointment chat does not exist.

        """
        try:
            return AppointmentChat.objects.get(pk=pk)
        except AppointmentChat.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Get the details of an appointment chat.

        Args:
            request (rest_framework.request.Request): The request object.
            pk (int): The ID of the appointment chat.

        Returns:
            rest_framework.response.Response: The response containing the serialized appointment chat.

        """
        appointment_chat = self.get_object(pk)
        serializer = AppointmentChatSerializer(appointment_chat)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an appointment chat.

        Args:
            request (rest_framework.request.Request): The request object.
            pk (int): The ID of the appointment chat.

        Returns:
            rest_framework.response.Response: The response containing the serialized updated appointment chat.

        """
        appointment_chat = self.get_object(pk)
        serializer = AppointmentChatSerializer(appointment_chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an appointment chat.

        Args:
            request (rest_framework.request.Request): The request object.
            pk (int): The ID of the appointment chat.

        Returns:
            rest_framework.response.Response: The response with a success status.

        """
        appointment_chat = self.get_object(pk)
        appointment_chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
