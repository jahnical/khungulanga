from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.disease import Disease
from api.serializers.disease import DiseaseSerializer


class DiseaseView(APIView):
    """
    API View to retrieve a list of diseases, create a new disease, update an existing disease, or delete a disease.
    """

    def get(self, request):
        """
        Retrieve a list of diseases.

        Returns:
        - Response: JSON response containing serialized data of all diseases.
        """
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new disease.

        Parameters:
        - request.data: JSON data containing the disease information.

        Returns:
        - Response: JSON response containing serialized data of the created disease.
        """
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing disease.

        Parameters:
        - pk (int): Primary key of the disease.
        - request.data: JSON data containing the updated disease information.

        Returns:
        - Response: JSON response containing serialized data of the updated disease.
        """
        disease = Disease.objects.get(pk=pk)
        serializer = DiseaseSerializer(disease, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a disease.

        Parameters:
        - pk (int): Primary key of the disease.

        Returns:
        - Response: HTTP response indicating successful deletion.
        """
        disease = Disease.objects.get(pk=pk)
        disease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiseaseDetail(APIView):
    """
    API View to retrieve details of a specific disease.
    """

    def get_object(self, pk):
        """
        Get a disease object based on its primary key.

        Parameters:
        - pk (int): Primary key of the disease.

        Returns:
        - Disease: Disease object with the given primary key.

        Raises:
        - Http404: If the disease does not exist.
        """
        try:
            return Disease.objects.get(pk=pk)
        except Disease.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve details of a specific disease.

        Parameters:
        - pk (int): Primary key of the disease.

        Returns:
        - Response: JSON response containing serialized data of the disease.
        """
        disease = self.get_object(pk)
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)
