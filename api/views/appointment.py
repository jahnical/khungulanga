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
    def get(self, request):
        is_patient = Patient.objects.all().filter(user=request.user).count() > 0
        appointments = (Appointment.objects.all().filter(patient_id=request.user.patient.id) if is_patient else Appointment.objects.all().filter(dermatologist_id=request.user.dermatologist.id))
        if (request.GET.get('cancelled', False) == 'false'):
            appointments = appointments.filter(done=True if request.GET.get('done', False) == 'true' else False)
        if is_patient:
            appointments = appointments.filter(patient_removed=None)
        else:
            appointments = appointments.filter(dermatologist_removed=None)
        if (request.GET.get('cancelled', False) == 'true'):
            appointments = appointments.exclude(patient_cancelled=None, dermatologist_cancelled=None)
        else:
            appointments = appointments.filter(patient_cancelled=None, dermatologist_cancelled=None)

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data

        # Extract the relevant fields from the request data
        dermatologist_id = data.get('dermatologist_id')
        patient_id = data.get('patient_id')
        book_date = data.get('book_date')
        appo_date = data.get('appo_date')
        done = data.get('done')
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
            done=False,
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
        
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
    
    
class AppointmentDetailView(APIView):
    def get(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)

        
        # request.data['patient'] = PatientSerializer(appointment.patient).data
        # request.data['patient']['gender'] = {"Male": "M",  "Female": "F", "Other": "O"}[request.data['patient']['gender']]
        # request.data['dermatologist'] = DermatologistSerializer(appointment.dermatologist).data
        # dg_id = request.data['diagnosis_id']
        # sd = DiagnosisSerializer(appointment.diagnosis).data if appointment.diagnosis else None
        # request.data['diagnosis'] = DiagnosisSerializer(Diagnosis.objects.get(pk=dg_id)).data if dg_id else sd
        
        if appointment.slot and (request.data['done'] == True or request.data['slot_id'] != appointment.slot.id):
            appointment.slot.scheduled = False
            appointment.slot.save()
            print("Slot set to unscheduled")
            if not request.data['done'] == True and (request.data['patient_cancelled'] or request.data['dermatologist_cancelled']):
                notify_appointment_cancelled(appointment, appointment.patient.user if request.user.is_staff else appointment.dermatologist.user, appointment.dermatologist.user if request.user.is_staff else appointment.patient.user)
                print("Appointment cancelled")
            if request.data['done'] == True and not appointment.done:
                notify_appointment_done(appointment, appointment.patient.user if request.user.is_staff else appointment.dermatologist.user, appointment.dermatologist.user if request.user.is_staff else appointment.patient.user)
                print("Appointment done")
        
        if request.data['slot_id']:
            slot = Slot.objects.get(pk=request.data['slot_id'])
            slot.scheduled = True
            slot.save()
        
        appointment.patient_removed = request.data['patient_removed'] if request.data['patient_removed'] else appointment.patient_removed
        appointment.dermatologist_removed = request.data['dermatologist_removed'] if request.data['dermatologist_removed'] else appointment.dermatologist_removed
        appointment.patient_cancelled = request.data['patient_cancelled'] if request.data['patient_cancelled'] else appointment.patient_cancelled
        appointment.dermatologist_cancelled = request.data['dermatologist_cancelled'] if request.data['dermatologist_cancelled'] else appointment.dermatologist_cancelled
        appointment.done = request.data['done'] == True if request.data['done'] else appointment.done
        appointment.slot_id = request.data['slot_id'] if request.data['slot_id'] else appointment.slot_id
        
        serializer = AppointmentSerializer(appointment)
        try:
            appointment.save()
            return Response(serializer.data)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        # print(request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)