from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.slot import Slot
from api.serializers.slot import SlotSerializer

class SlotAPIView(APIView):
    def get(self, request):
        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request):
        start_time = request.data.get('start_time')
        dermatologist_id = request.data.get('dermatologist_id')
        scheduled = request.data.get('scheduled', False)
        day_of_week = request.data.get('day_of_week')

        slot = Slot(start_time=start_time, dermatologist_id=dermatologist_id, scheduled=scheduled, day_of_week=day_of_week)
        slot.save()

        return Response({'id': slot.id, 'start_time': slot.start_time, 'dermatologist_id': slot.dermatologist_id,
                         'scheduled': slot.scheduled, 'day_of_week': slot.day_of_week},
                        status=status.HTTP_201_CREATED)

class SlotDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot)
        return Response(serializer.data)

    def put(self, request, pk):
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        slot = self.get_object(pk)
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
