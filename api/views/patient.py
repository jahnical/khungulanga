import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from api.models.patient import Patient
from api.serializers.patient import PatientSerializer


class PatientView(APIView):
    """
    API View to retrieve a list of all patients and create a new patient.
    """

    def get(self, request):
        """
        Retrieve a list of all patients.

        Returns:
        - Response: JSON response containing serialized data of all patients.
        """
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new patient.

        Parameters:
        - request.data: JSON data containing the patient information.

        Returns:
        - Response: JSON response containing serialized data of the created patient.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        """
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    """
    API View to retrieve, update, and delete a specific patient.
    """

    def get_object(self, username):
        """
        Get the patient object with the specified username.

        Parameters:
        - username (str): Username of the patient.

        Returns:
        - Patient: The patient object.

        Raises:
        - Http404: If the patient does not exist.
        """
        try:
            user = User.objects.get(username=username)
            return Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, username):
        """
        Retrieve the details of a specific patient.

        Parameters:
        - username (str): Username of the patient.

        Returns:
        - Response: JSON response containing serialized data of the patient.

        Raises:
        - Http404: If the patient does not exist.
        """
        patient = self.get_object(username)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, username):
        """
        Update the details of a specific patient.

        Parameters:
        - username (str): Username of the patient.
        - request.data: JSON data containing the updated patient information.

        Returns:
        - Response: JSON response containing serialized data of the updated patient.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        - Http404: If the patient does not exist.
        """
        patient = self.get_object(username)
        patient.dob = datetime.datetime.strptime(request.data['dob'], '%Y-%m-%dT%H:%M:%S.%f') if request.data['dob'] else patient.dob
        patient.gender = request.data['gender'] if request.data['gender'] else patient.dob
        
        user = patient.user
        user.first_name = request.data['first_name'] if request.data['first_name'] else user.first_name
        user.last_name = request.data['last_name'] if request.data['last_name'] else user.last_name
        user.email = request.data['email'] if request.data['email'] else user.email
        
        serializer = PatientSerializer(patient)
        try:
            user.save()
            patient.save()
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        """
        Delete a specific patient.

        Parameters:
        - username (str): Username of the patient.

        Returns:
        - Response: Empty response with HTTP status code 204 (No Content).

        Raises:
        - Http404: If the patient does not exist.
        """
        patient = self.get_object(username)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
