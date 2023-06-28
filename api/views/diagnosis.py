import traceback
import numpy as np
from api.models.dermatologist import Dermatologist
import api.models.prediction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core import serializers
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
    API View to create or get a list of all the diagnoses of users.
    GET request returns the user's diagnoses, whereas a POST request allows creating a new diagnosis.
    """
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, format=None):
        # If the user is a staff member, retrieve pending diagnoses associated with the dermatologist
        if (not request.user == None) and request.user.is_staff:
            diagnoses = request.user.dermatologist.diagnosis_set.all().filter(action='Pending')
            return JsonResponse(DiagnosisSerializer(diagnoses, many=True).data, safe=False)
        # If the user is a patient, retrieve their diagnoses
        if not request.user == None:
            diagnoses = request.user.patient.diagnosis_set.all()
            return JsonResponse(DiagnosisSerializer(diagnoses, many=True).data, safe=False)
        # If the user is not authorized, return an error response
        return Response({'error': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def _fetch_diagnosis(self, id):
        # Helper method to fetch a diagnosis object based on its ID
        diagnosis = get_object_or_404(Diagnosis.objects.select_related('prediction_set', 'prediction_se'), pk=id)
        return diagnosis
    
    def post(self, request, format=None):
        """
        Create a new diagnosis.

        Parameters:
        - image_path (str): Path to the image file.
        - user (User): User object representing the patient.
        - body_part (str): Body part associated with the diagnosis.
        - itchy (bool): Indicates if the condition is itchy or not.

        Returns:
        - JsonResponse: JSON response containing the serialized diagnosis object.
        """
        # Handle the POST request to create a new diagnosis
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
            # Create a new diagnosis object
            diagnosis = Diagnosis.objects.create(**{
                "image": image_path,
                "patient": user.patient,
                "body_part": body_part,
                "itchy": itchy
            })
            # Perform disease prediction on the diagnosis
            predict_disease(diagnosis)
            return JsonResponse(DiagnosisSerializer(diagnosis).data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiagnosisDetailView(APIView):
    """
    API View to update or delete a specific diagnosis.
    """
    
    def put(self, request, pk):
        """
        Update a diagnosis.

        Parameters:
        - pk (int): Primary key of the diagnosis.

        Returns:
        - JsonResponse: JSON response containing the serialized diagnosis object.
        """
        # Handle the PUT request to update a diagnosis
        diagnosis = Diagnosis.objects.get(pk=pk)
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
        """
        Delete a diagnosis.

        Parameters:
        - pk (int): Primary key of the diagnosis.

        Returns:
        - Response: HTTP response indicating successful deletion.
        """
        # Handle the DELETE request to delete a diagnosis
        diagnosis = Diagnosis.objects.get(pk=pk)
        diagnosis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
