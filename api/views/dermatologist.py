import json
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from api.models.clinic import Clinic
from api.models.dermatologist import Dermatologist
from api.serializers.dermatologist import DermatologistSerializer
from django.core import serializers

class DermatologistView(APIView):
    
    permission_classes = []
    
    def get(self, request):
        dermatologists = Dermatologist.objects.all()
        serializer = DermatologistSerializer(dermatologists, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        qualification = data.get('qualification', None)
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)
        clinic_name = data.get('clinic[name]', None)
        clinic_lat = data.get('clinic[latitude]', None)
        clinic_lon = data.get('clinic[longitude]', None)
        specialization = data.get('specialization', None)
        hourly_rate = data.get('hourly_rate', None)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Create the user object
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        
        dermatologist = Dermatologist.objects.create(
            user=user,
            qualification=qualification,
            email=email,
            phone_number=phone_number,
            clinic=Clinic.objects.create(name=clinic_name, latitude=clinic_lat, longitude=clinic_lon),
            specialization=specialization,
            hourly_rate=hourly_rate
        )
        dermatologist.save()

        if user:
            return JsonResponse(
                serializers.serialize("json", [user, dermatologist]),
                status=status.HTTP_201_CREATED,
                safe=False
            )
        return Response(
            {
                "error": True,
                "error_msg": user,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class DermatologistDetail(APIView):
    def get_object(self, username):
        try:
            user = User.objects.get(username=username)
            return Dermatologist.objects.get(user=user)
        except Dermatologist.DoesNotExist:
            raise Http404

    def get(self, request, username):
        dermatologist = self.get_object(username)
        serializer = DermatologistSerializer(dermatologist)
        return Response(serializer.data)

    def put(self, request, pk):
        dermatologist = self.get_object(pk)
        serializer = DermatologistSerializer(dermatologist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        dermatologist = self.get_object(pk)
        dermatologist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
