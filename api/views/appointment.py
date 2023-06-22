from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.appointment import Appointment
from api.models.diagnosis import Diagnosis
from api.models.patient import Patient
from api.models.slot import Slot
from api.serializers.appointment import AppointmentSerializer
from api.serializers.dermatologist import DermatologistSerializer
from api.serializers.diagnosis import DiagnosisSerializer
from api.serializers.patient import PatientSerializer
from api.util.notifications import notify_appointment_booked, notify_appointment_cancelled

class AppointmentView(APIView):
    def get(self, request):
        is_patient = Patient.objects.all().filter(user=request.user).count() > 0
        appointments = (Appointment.objects.all().filter(patient_id=request.user.patient.id) if is_patient else Appointment.objects.all().filter(dermatologist_id=request.user.dermatologist.id)).filter(
            done= True if request.GET.get('done', False) == 'true' else False)
        if is_patient:
            appointments = appointments.filter(patient_removed=None)
        else:
            appointments = appointments.filter(dermatologist_removed=None)
        if (request.GET.get('cancelled', False) == 'true'):
            appointments = appointments.filter(patient_cancelled=True if is_patient else False).filter(dermatologist_cancelled=False if is_patient else True)
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
    
    # Implement other methods such as PUT, DELETE, etc.
    # Example:
    def put(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        request.data['patient'] = PatientSerializer(appointment.patient).data
        request.data['patient']['gender'] = {"Male": "M",  "Female": "F", "Other": "O"}[request.data['patient']['gender']]
        request.data['dermatologist'] = DermatologistSerializer(appointment.dermatologist).data
        app_id = request.data['diagnosis_id']
        sd = DiagnosisSerializer(appointment.diagnosis).data if appointment.diagnosis else None
        request.data['diagnosis'] = DiagnosisSerializer(Diagnosis.objects.get(pk=app_id)).data if app_id else sd
        if appointment.slot and (request.data['done'] == 'true' or request.data['slot_id'] != appointment.slot.id):
            slot = Slot.objects.get(pk=appointment.slot.id)
            slot.scheduled = False
            slot.save()
            if not request.data['done'] == 'true' and (request.data['patient_cancelled'] == 'true' or request.data['dermatologist_cancelled'] == 'true'):
                notify_appointment_cancelled(appointment)
        
        if request.data['slot_id']:
            slot = Slot.objects.get(pk=request.data['slot_id'])
            slot.scheduled = True
            slot.save()
        
            
        serializer = AppointmentSerializer(appointment, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
