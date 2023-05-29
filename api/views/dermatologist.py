import json
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
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
        data = json.loads(request.body)
        qualification = data.pop('qualification')
        email = data.pop('email')
        phone_number = data.pop('phone_number')
        clinic = data.pop('clinic')
        location_lat = data.pop('location_lat')
        location_lon = data.pop('location_lon')
        location_desc = data.pop('location_desc')

        user = User.objects.create_user(**data)
        dermatologist = Dermatologist.objects.create(
            user=user,
            qualification=qualification,
            email=email,
            phone_number=phone_number,
            clinic=clinic,
            location_lat=location_lat,
            location_lon=location_lon,
            location_desc=location_desc
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
    def get_object(self, pk):
        try:
            return Dermatologist.objects.get(pk=pk)
        except Dermatologist.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dermatologist = self.get_object(pk)
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
