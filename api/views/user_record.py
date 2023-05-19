import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
import json
from api.models.patient import Patient

class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = []
    
    def get(self, format=None):
        users = User.objects.all()
        return JsonResponse(serializers.serialize("json", users), safe=False)

    def post(self, request):
        data = json.loads(request.body)
        dob = data.pop('dob')
        print(dob)
        dob = datetime.datetime.strptime(dob, '%Y-%m-%dT%H:%M:%S.%f')
        gender = data.pop('gender')

        user = User.objects.create_user(**data)
        patient = Patient.objects.create(user=user, dob=dob, gender=gender)
        patient.save()
        if user:
            return JsonResponse(
                serializers.serialize("json", [user, patient]),
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