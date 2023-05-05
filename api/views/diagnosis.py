from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from api.skindisease import predict_disease
import json
from api.models.diagnosis import Diagnosis
from api.models.patient import Patient


class DiagnosisView(APIView):
    """
    API View to create or get a list of all the diagnoses of
    users. GET request returns the user's diagnoses whereas
    a POST request allows to create a new diagnosis.
    """
    parser_classes = [MultiPartParser, FormParser]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        diagnoses = request.user.patient.diagnosis_set.all()
        return JsonResponse(serializers.serialize("json", diagnoses), safe=False)

    def post(self, request, format=None):
        image = request.data.get('image', None)
        user = request.user
        body_part = request.data.get('body_part', None)
        itchy = request.data.get('itchy', None)
        
        if image is None:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        predictions = predict_disease(image, body_part, itchy)
        
        # diagnosis = Diagnosis.objects.create({
        #     "image": image,
        #     "patient": user.patient,
        #     "body_part": body_part,
        #     "itchy": itchy
        # })
        
        # for p in predictions:
        #     p.diagnosis = diagnosis
        #     p.save()

        # Return a response with a success status code
        return JsonResponse(json.dumps(predictions), safe=False)