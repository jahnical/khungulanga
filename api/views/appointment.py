import datetime
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
from api.util.notifications import (
    notify_appointment_booked,
    notify_appointment_cancelled,
    notify_appointment_done,
)



class AppointmentView(APIView):
    """
    API endpoint for managing appointments.
    """

    def get(self, request):
        """
        Retrieve a list of appointments.

        Optional query parameters:
        - cancelled: Filter appointments by cancellation status ('true' or 'false')
        - done: Filter appointments by completion status ('true' or 'false')

        Returns:
        - List of appointments in the response body.
        """
        is_patient = Patient.objects.filter(user=request.user).exists()
        appointments = (
            Appointment.objects.filter(patient_id=request.user.patient.id)
            if is_patient
            else Appointment.objects.filter(dermatologist_id=request.user.dermatologist.id)
        )
        
        for appointment in appointments:
            if appointment.appo_date.date() < datetime.date.today():
                appointment.slot.scheduled = False
                appointment.slot.save()
                appointment.done = True
                appointment.slot = None
                appointment.save()

        if request.GET.get('cancelled', False) == 'false':
            appointments = appointments.filter(
                done=True if request.GET.get('done', False) == 'true' else False
            )

        if is_patient:
            appointments = appointments.exclude(patient_removed__isnull=False)
        else:
            appointments = appointments.filter(dermatologist_removed=None)

        if request.GET.get('cancelled', False) == 'true':
            appointments = appointments.exclude(
                patient_cancelled=None, dermatologist_cancelled=None
            )
        else:
            appointments = appointments.filter(
                patient_cancelled=None, dermatologist_cancelled=None
            )

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new appointment.

        Request body should contain the following fields:
        - dermatologist_id: ID of the dermatologist
        - patient_id: ID of the patient
        - book_date: Booking date
        - appo_date: Appointment date
        - done: Completion status ('true' or 'false')
        - duration: Duration of the appointment
        - cost: Cost of the appointment
        - extra_info: Additional information about the appointment
        - patient_removed: Date and time when the patient was removed from the appointment
        - dermatologist_removed: Date and time when the dermatologist was removed from the appointment
        - patient_cancelled: Date and time when the patient cancelled the appointment
        - dermatologist_cancelled: Date and time when the dermatologist cancelled the appointment
        - diagnosis_id: ID of the diagnosis (optional)
        - slot_id: ID of the time slot

        Returns:
        - Created appointment in the response body.
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
            slot_id=slot_id,
        )

        slot = Slot.objects.get(pk=slot_id)
        slot.scheduled = True
        slot.save()

        notify_appointment_booked(appointment)

        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)


class AppointmentDetailView(APIView):
    """
    API endpoint for managing individual appointments.
    """

    def get(self, request, pk):
        """
        Retrieve an appointment by ID.

        Args:
        - pk: ID of the appointment

        Returns:
        - Retrieved appointment in the response body.
        """
        appointment = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an appointment by ID.

        Args:
        - pk: ID of the appointment

        Request body can contain the following fields to update:
        - done: Completion status ('true' or 'false')
        - slot_id: ID of the time slot
        - patient_removed: Date and time when the patient was removed from the appointment
        - dermatologist_removed: Date and time when the dermatologist was removed from the appointment
        - patient_cancelled: Date and time when the patient cancelled the appointment
        - dermatologist_cancelled: Date and time when the dermatologist cancelled the appointment

        Returns:
        - Updated appointment in the response body.
        """
        appointment = Appointment.objects.get(pk=pk)

        if appointment.slot and (
            request.data['done'] == True or request.data['slot_id'] != appointment.slot.id
        ):
            appointment.slot.scheduled = False
            appointment.slot.save()
            print("Slot set to unscheduled")
            if not request.data['done'] == True and (
                request.data['patient_cancelled'] or request.data['dermatologist_cancelled']
            ):
                notify_appointment_cancelled(
                    appointment,
                    appointment.patient.user
                    if request.user.is_staff
                    else appointment.dermatologist.user,
                    appointment.dermatologist.user
                    if request.user.is_staff
                    else appointment.patient.user,
                )
                print("Appointment cancelled")
            if request.data['done'] == True and not appointment.done:
                notify_appointment_done(
                    appointment,
                    appointment.patient.user
                    if request.user.is_staff
                    else appointment.dermatologist.user,
                    appointment.dermatologist.user
                    if request.user.is_staff
                    else appointment.patient.user,
                )
                print("Appointment done")

        if request.data['slot_id']:
            slot = Slot.objects.get(pk=request.data['slot_id'])
            slot.scheduled = True
            slot.save()

        appointment.patient_removed = (
            request.data['patient_removed']
            if request.data['patient_removed']
            else appointment.patient_removed
        )
        appointment.dermatologist_removed = (
            request.data['dermatologist_removed']
            if request.data['dermatologist_removed']
            else appointment.dermatologist_removed
        )
        appointment.patient_cancelled = (
            request.data['patient_cancelled']
            if request.data['patient_cancelled']
            else appointment.patient_cancelled
        )
        appointment.dermatologist_cancelled = (
            request.data['dermatologist_cancelled']
            if request.data['dermatologist_cancelled']
            else appointment.dermatologist_cancelled
        )
        appointment.done = request.data['done'] == True if request.data['done'] else appointment.done
        appointment.slot_id = (
            request.data['slot_id'] if request.data['slot_id'] else appointment.slot_id
        )

        serializer = AppointmentSerializer(appointment)
        try:
            appointment.save()
            return Response(serializer.data)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an appointment by ID.

        Args:
        - pk: ID of the appointment

        Returns:
        - Empty response with status code 204 (No Content).
        """
        appointment = Appointment.objects.get(pk=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
