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
    API View to create or get a list of all the registered users.
    GET request returns the registered users, whereas a POST request allows creating a new user.
    """
    permission_classes = []

    def get(self, format=None):
        """
        Get the list of all registered users.

        Returns:
        - JsonResponse: JSON response containing serialized data of all users.
        """
        users = User.objects.all()
        return JsonResponse(serializers.serialize("json", users), safe=False)

    def post(self, request):
        """
        Create a new user.

        Parameters:
        - request.body: JSON data containing the user information.
          - username (str): The username of the user.
          - password (str): The password of the user.
          - dob (str): The date of birth of the user in the format 'YYYY-MM-DDTHH:MM:SS.ssssss'.
          - gender (str): The gender of the user.

        Returns:
        - JsonResponse: JSON response containing serialized data of the created user and associated patient.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        """
        data = json.loads(request.body)
        dob = data.pop('dob')
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
