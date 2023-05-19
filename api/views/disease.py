from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.disease import Disease
from api.serializers.disease import DiseaseSerializer


class DiseaseView(APIView):
    def get(self, request):
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        disease = Disease.objects.get(pk=pk)
        serializer = DiseaseSerializer(disease, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        disease = Disease.objects.get(pk=pk)
        disease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DiseaseDetail(APIView):
    def get_object(self, pk):
        try:
            return Disease.objects.get(pk=pk)
        except Disease.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        disease = self.get_object(pk)
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)