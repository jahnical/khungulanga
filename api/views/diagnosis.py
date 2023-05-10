import numpy as np
import api.models.prediction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core import serializers
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from api.skindisease import detect_skin, predict_disease
import json
from api.models.diagnosis import Diagnosis, DiagnosisSerializer
from PIL import Image



class DiagnosisView(APIView):
    """
    API View to create or get a list of all the diagnoses of
    users. GET request returns the user's diagnoses whereas
    a POST request allows to create a new diagnosis.
    """
    parser_classes = [MultiPartParser, FormParser]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        if not request.user == None and request.user.is_staff:
            diagnoses = request.user.patient.diagnosis_set.all()
            return JsonResponse(DiagnosisSerializer(diagnoses, many=True), safe=False)
        if not request.user == None:
            diagnoses = request.user.patient.diagnosis_set.all()
            return JsonResponse(DiagnosisSerializer(diagnoses, many=True).data, safe=False)
        return Response({'error': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
    def _fetch_diagnosis(self, id):
        diagnosis = get_object_or_404(Diagnosis.objects.select_related('prediction_set', 'prediction_se'), pk=id)
        return diagnosis
    
    def post(self, request, format=None):
        image_path = request.data.get('image', None)
        user = request.user
        body_part = request.data.get('body_part', None)
        itchy = True if request.data.get('itchy', None) == "true" else False
        
        if image_path is None:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image = np.asarray(Image.open(image_path))
        has_skin = detect_skin(image=image)
        if not has_skin:
             return Response({'error': "No skin detected"}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            diagnosis = Diagnosis.objects.create(**{
                "image": image_path,
                "patient": user.patient,
                "body_part": body_part,
                "itchy": itchy
            })
            predict_disease(diagnosis)
            return JsonResponse(DiagnosisSerializer(diagnosis).data, safe=False, status=status.HTTP_200_OK)
            #return JsonResponse(json.dumps(self._map_to_dict(diagnosis, predictions)), safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        diagnosis = Diagnosis.objects.get(pk=pk)
        diagnosis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)