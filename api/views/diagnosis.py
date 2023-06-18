import traceback
import numpy as np
from api.models.dermatologist import Dermatologist
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
from api.serializers.diagnosis import DiagnosisSerializer
from api.skindisease import detect_skin, predict_disease
import json
from api.models.diagnosis import Diagnosis
from PIL import Image

from api.util.notifications import notify_diagnosis_to_confirm, notify_diagnosis_feedback

class DiagnosisView(APIView):
    """
    API View to create or get a list of all the diagnoses of
    users. GET request returns the user's diagnoses whereas
    a POST request allows to create a new diagnosis.
    """
    parser_classes = [MultiPartParser, FormParser]
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        if (not request.user == None) and request.user.is_staff:
            diagnoses = request.user.dermatologist.diagnosis_set.all().filter(action='Pending')
            return JsonResponse(DiagnosisSerializer(diagnoses, many=True).data, safe=False)
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
        if not has_skin and request.data.get('ignore_skin', "false") == "false":
             return Response({'error': "No skin detected"}, status=status.HTTP_206_PARTIAL_CONTENT)
        
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
        

class DiagnosisDetailView(APIView):
    
    def put(self, request, pk):
        diagnosis = Diagnosis.objects.get(pk=pk)
        print(request.headers)
        print(request.content_type)
        if diagnosis is None:
            print("Diagnosis not found")
            return Response({'error': 'Diagnosis not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            print(request.data)
        except Exception as e:
            traceback.print_exc()
        # Update the diagnosis fields from the request data
        dermatologist_id = request.data.get('dermatologist_id')
        extra_derm_info = request.data.get('extra_derm_info', diagnosis.extra_derm_info)
        approved = request.data.get('approved', diagnosis.approved)
        action = request.data.get('action', diagnosis.action)
        
        if (not diagnosis.dermatologist_id == dermatologist_id) and (dermatologist_id is not None):
            dermatologist = get_object_or_404(Dermatologist, pk=dermatologist_id)
            notify_diagnosis_to_confirm(diagnosis, dermatologist)
            
        if (not diagnosis.approved == approved) or (not diagnosis.action == action):
            notify_diagnosis_feedback(diagnosis)
        
        # Update the diagnosis object with the new values
        diagnosis.dermatologist_id = dermatologist_id
        diagnosis.extra_derm_info = extra_derm_info
        diagnosis.approved = approved
        diagnosis.action = action
        diagnosis.save()
        
        return JsonResponse(DiagnosisSerializer(diagnosis).data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        diagnosis = Diagnosis.objects.get(pk=pk)
        diagnosis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)