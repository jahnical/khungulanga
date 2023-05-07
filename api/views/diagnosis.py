from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
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
    
    def _fetch_diagnosis(self, id):
        diagnosis = get_object_or_404(Diagnosis.objects.select_related('prediction_set', 'prediction_se'), pk=id)
        return diagnosis

    def post(self, request, format=None):
        image = request.data.get('image', None)
        user = request.user
        body_part = request.data.get('body_part', None)
        itchy = True if request.data.get('itchy', None) == "true" else False
        
        if image is None:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        diagnosis = Diagnosis.objects.create(**{
            "image": image,
            "patient": user.patient,
            "body_part": body_part,
            "itchy": itchy
        })
        
        predictions = predict_disease(diagnosis)
        
        data = {
            "image": diagnosis.image.url,
            "body_part": diagnosis.body_part,
            "itchy": diagnosis.itchy,
            "date": diagnosis.date.strftime("%Y-%m-%d %H:%M:%S"),
            "predictions": [
                {
                    "disease": {
                        "name": prediction.disease.name,
                        "description": prediction.disease.description,
                        "severity": prediction.disease.get_severity_display(),
                        "treatments": [
                            {
                                "description": treatment.description,
                                "title": treatment.title,
                            } for treatment in prediction.disease.treatment_set.all()], 
                    },
                    "probability": prediction.probability,
                } for prediction in predictions
            ]
        }
        
        return JsonResponse(json.dumps(data), safe=False, status=status.HTTP_200_OK)