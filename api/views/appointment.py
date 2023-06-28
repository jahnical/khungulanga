from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from api.models.appointment import Appointment
from api.models.diagnosis import Diagnosis
from api.models.patient import Patient
from api.models.slot import Slot
from api.serializers.appointment import AppointmentSerializer
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.patient import PatientSerializer
from api.util.notifications import notify_appointment_booked, notify_appointment_cancelled, notify_appointment_done


class AppointmentView(APIView):
    """
    API view for retrieving and creating appointments.
    """

    def get(self, request):
        """
        Retrieve a list of appointments based on the user type and filters.

        Available filters:
        - cancelled: (bool) Filter by cancelled status (default: False)
        - done: (bool) Filter by done status (default: False)

        For patients:
        - Exclude appointments where patient_removed is not None.

        For dermatologists:
        - Exclude appointments where dermatologist_removed is not None.

        Excluded appointments are those that have been removed by the respective party.

        Returns:
        - List of serialized appointment data.
        """
        is_patient = Patient.objects.filter(user=request.user).exists()
        appointments = (
            Appointment.objects.filter(patient_id=request.user.patient.id)
            if is_patient
            else Appointment.objects.filter(dermatologist_id=request.user.dermatologist.id)
        )

        cancelled = request.GET.get('cancelled', False) == 'true'
        done = request.GET.get('done', False) == 'true'

        # Apply filters
        appointments = appointments.filter(done=done)
        if is_patient:
            appointments = appointments.exclude(patient_removed__isnull=False)
        else:
            appointments = appointments.exclude(dermatologist_removed__isnull=False)

        if cancelled:
            appointments = appointments.exclude(
                Q(patient_cancelled__isnull=False) & Q(dermatologist_cancelled__isnull=False)
            )
        else:
            appointments = appointments.filter(
                Q(patient_cancelled__isnull=True) | Q(dermatologist_cancelled__isnull=True)
            )

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new appointment.

        Request data should contain the following fields:
        - dermatologist_id (int): ID of the dermatologist.
        - patient_id (int): ID of the patient.
        - book_date (str): Booking date.
        - appo_date (str): Appointment date.
        - done (bool): Done status.
        - duration (int): Duration of the appointment.
        - cost (float): Cost of the appointment.
        - extra_info (str): Additional information.
        - patient_removed (bool): Patient removed status (optional).
        - dermatologist_removed (bool): Dermatologist removed status (optional).
        - patient_cancelled (bool): Patient cancelled status (optional).
        - dermatologist_cancelled (bool): Dermatologist cancelled status (optional).
        - diagnosis_id (int): ID of the diagnosis (optional).
        - slot_id (int): ID of the slot.

        Returns:
        - Serialized data of the created appointment.
        """
        data = request.data

        # Extract the relevant fields from the request data
        dermatologist_id = data.get('dermatologist_id')
        patient_id = data.get('patient_id')
        book_date = data.get('book_date')
        appo_date = data.get('appo_date')
        done = data.get('done', False)
        duration = data.get('duration')
        cost = data.get('cost')
        extra_info = data.get('extra_info')
        patient_removed = data.get('patient_removed')
        dermatologist_removed = data.get('dermatologist_removed')
        patient_cancelled = data.get('patient_cancelled')
        dermatologist_cancelled = data.get('dermatologist_cancelled')
        diagnosis_id = data.get('diagnosis_id')
        slot_id = data.get('slot_id')

        # Create the Appointment object
        appointment = Appointment.objects.create(
            dermatologist_id=dermatologist_id,
            patient_id=patient_id,
            book_date=book_date,
            appo_date=appo_date,
            done=done,
            duration=duration,
            cost=cost,
            extra_info=extra_info,
            patient_removed=patient_removed,
            dermatologist_removed=dermatologist_removed,
            patient_cancelled=patient_cancelled,
            dermatologist_cancelled=dermatologist_cancelled,
            diagnosis_id=diagnosis_id,
            slot_id=slot_id
        )

        slot = Slot.objects.get(pk=slot_id)
        slot.scheduled = True
        slot.save()

        notify_appointment_booked(appointment)

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentDetailView(APIView):
    """
    API view for retrieving, updating, and deleting individual appointments.
    """

    def get(self, request, pk):
        """
        Retrieve an individual appointment based on the ID.

        Args:
        - pk (int): ID of the appointment.

        Returns:
        - Serialized data of the appointment.
        """
        appointment = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an individual appointment based on the ID.

        Args:
        - pk (int): ID of the appointment.

        Request data should contain the following fields:
        - patient_removed (bool): Patient removed status (optional).
        - dermatologist_removed (bool): Dermatologist removed status (optional).
        - patient_cancelled (bool): Patient cancelled status (optional).
        - dermatologist_cancelled (bool): Dermatologist cancelled status (optional).
        - done (bool): Done status (optional).
        - slot_id (int): ID of the slot (optional).

        Returns:
        - Serialized data of the updated appointment.
        """
        appointment = Appointment.objects.get(pk=pk)

        # Update the appointment fields
        appointment.patient_removed = request.data.get('patient_removed', appointment.patient_removed)
        appointment.dermatologist_removed = request.data.get('dermatologist_removed', appointment.dermatologist_removed)
        appointment.patient_cancelled = request.data.get('patient_cancelled', appointment.patient_cancelled)
        appointment.dermatologist_cancelled = request.data.get('dermatologist_cancelled', appointment.dermatologist_cancelled)
        appointment.done = request.data.get('done', appointment.done)
        appointment.slot_id = request.data.get('slot_id', appointment.slot_id)

        # Handle slot changes and appointment status updates
        if appointment.slot and (appointment.done != request.data.get('done', appointment.done) or
                                 appointment.slot_id != request.data.get('slot_id', appointment.slot_id)):
            appointment.slot.scheduled = False
            appointment.slot.save()

            if not appointment.done and (appointment.patient_cancelled or appointment.dermatologist_cancelled):
                notify_appointment_cancelled(
                    appointment,
                    appointment.patient.user if request.user.is_staff else appointment.dermatologist.user,
                    appointment.dermatologist.user if request.user.is_staff else appointment.patient.user
                )

            if appointment.done and not appointment.done:
                notify_appointment_done(
                    appointment,
                    appointment.patient.user if request.user.is_staff else appointment.dermatologist.user,
                    appointment.dermatologist.user if request.user.is_staff else appointment.patient.user
                )

        if request.data.get('slot_id'):
            slot = Slot.objects.get(pk=request.data['slot_id'])
            slot.scheduled = True
            slot.save()

        serializer = AppointmentSerializer(appointment)
        try:
            appointment.save()
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an individual appointment based on the ID.

        Args:
        - pk (int): ID of the appointment.

        Returns:
        - HTTP 204 No Content if the deletion is successful.
        """
        appointment = Appointment.objects.get(pk=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
