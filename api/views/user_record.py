from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
import json


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    # permission_classes = [IsAdminUser]
    
    def get(self, format=None):
        users = User.objects.all()
        return JsonResponse(users)

    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create_user(**data)
        if user.is_valid(raise_exception=ValueError):
            return JsonResponse(
                user,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": user.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )