from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.prediction import Prediction
from api.serializers.prediction import PredictionSerializer

class PredictionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all predictions
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            prediction = Prediction.objects.get(pk=pk)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PredictionSerializer(prediction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            prediction = Prediction.objects.get(pk=pk)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PredictionSerializer(prediction, data=request.data, partial=True)
        serializer.save()
        return Response(serializer.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            prediction = Prediction.objects.get(pk=pk)
        except Prediction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
