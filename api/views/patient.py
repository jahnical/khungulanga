import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from api.models.patient import Patient
from api.serializers.patient import PatientSerializer

class PatientView(APIView):
    
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientDetail(APIView):
    def get_object(self, username):
        try:
            user = User.objects.get(username=username)
            return Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, username):
        patient = self.get_object(username)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, username):
        patient = self.get_object(username)
        patient.dob = datetime.datetime.strptime(request.data['dob'], '%Y-%m-%dT%H:%M:%S.%f') if request.data['dob'] else patient.dob
        patient.gender = request.data['gender'] if request.data['gender'] else patient.dob
        
        user = patient.user
        user.first_name = request.data['first_name'] if request.data['first_name'] else user.first_name
        user.last_name = request.data['last_name'] if request.data['last_name'] else user.last_name
        user.email = request.data['email'] if request.data['email'] else user.email
        
        serializer = PatientSerializer(patient)
        try:
            user.save()
            patient.save()
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        patient = self.get_object(username)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
