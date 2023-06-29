from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.disease import Disease
from api.models.prediction import Prediction
from api.serializers.prediction import PredictionSerializer


class PredictionAPIView(APIView):
    """
    API View to retrieve, create, update, and delete predictions.
    """

    def get(self, request, *args, **kwargs):
        """
        Retrieve all predictions.

        Returns:
        - Response: JSON response containing serialized data of all predictions.
        """
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new prediction.

        Parameters:
        - request.data: JSON data containing the prediction information.

        Returns:
        - Response: JSON response containing serialized data of the created prediction.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        """
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """
        Update an existing prediction.

        Parameters:
        - pk (int): The primary key of the prediction.
        - request.data: JSON data containing the updated prediction information.

        Returns:
        - Response: JSON response containing serialized data of the updated prediction.

        Raises:
        - status.HTTP_404_NOT_FOUND: If the prediction does not exist.
        - status.HTTP_400_BAD_REQUEST: If the disease_id is invalid.
        """
        try:
            prediction = Prediction.objects.get(pk=pk)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Fetch the disease object based on the disease_id
        disease_id = request.data.get('disease_id')
        try:
            disease = Disease.objects.get(pk=disease_id)
        except Disease.DoesNotExist:
            return Response({'error': 'Invalid disease_id'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the serializer data with the fetched disease object
        serializer_data = request.data.copy()
        serializer_data['disease'] = disease.id
        
        print(serializer_data)
        
        serializer = PredictionSerializer(prediction, data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        """
        Partially update an existing prediction.

        Parameters:
        - pk (int): The primary key of the prediction.
        - request.data: JSON data containing the updated prediction information.

        Returns:
        - Response: JSON response containing serialized data of the updated prediction.

        Raises:
        - status.HTTP_404_NOT_FOUND: If the prediction does not exist.
        """
        try:
            prediction = Prediction.objects.get(pk=pk)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PredictionSerializer(prediction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete an existing prediction.

        Parameters:
        - pk (int): The primary key of the prediction.

        Returns:
        - Response: Empty response with HTTP status code 204 (No Content).

        Raises:
        - status.HTTP_404_NOT_FOUND: If the prediction does not exist.
        """
        try:
            prediction = Prediction.objects.get(pk=pk)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
