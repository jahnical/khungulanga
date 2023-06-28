from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.dermatologist import Dermatologist
from api.models.slot import Slot
from api.serializers.slot import SlotSerializer


class SlotAPIView(APIView):
    """
    API View to retrieve slots, create a new slot.
    """

    def get(self, request, derm_id):
        """
        Retrieve all slots for a dermatologist.

        Parameters:
        - derm_id (int): The primary key of the dermatologist.

        Returns:
        - Response: JSON response containing serialized data of the slots.
        """
        slots = Slot.objects.filter(dermatologist_id=derm_id)
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new slot.

        Parameters:
        - request.data: JSON data containing the slot information.
          - start_time (datetime): The start time of the slot.
          - dermatologist_id (int): The primary key of the dermatologist associated with the slot.
          - scheduled (bool): Indicates whether the slot is scheduled or not (default is False).
          - day_of_week (str): The day of the week for the slot.

        Returns:
        - Response: JSON response containing serialized data of the created slot.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        """
        start_time = request.data.get('start_time')
        dermatologist_id = request.data.get('dermatologist_id')
        scheduled = request.data.get('scheduled', False)
        day_of_week = request.data.get('day_of_week')

        slot = Slot(start_time=start_time, dermatologist_id=dermatologist_id, scheduled=scheduled, day_of_week=day_of_week)
        slot.save()

        return Response(
            {
                'id': slot.id,
                'start_time': slot.start_time,
                'dermatologist_id': slot.dermatologist_id,
                'scheduled': slot.scheduled,
                'day_of_week': slot.day_of_week
            },
            status=status.HTTP_201_CREATED
        )


class SlotDetailAPIView(APIView):
    """
    API View to retrieve, update, and delete a specific slot.
    """

    def get_object(self, pk):
        """
        Get the slot object based on the primary key.

        Parameters:
        - pk (int): The primary key of the slot.

        Returns:
        - Slot: The slot object.

        Raises:
        - Http404: If the slot does not exist.
        """
        try:
            return Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a specific slot.

        Parameters:
        - pk (int): The primary key of the slot.

        Returns:
        - Response: JSON response containing serialized data of the slot.

        Raises:
        - Http404: If the slot does not exist.
        """
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific slot.

        Parameters:
        - pk (int): The primary key of the slot.
        - request.data: JSON data containing the updated slot information.

        Returns:
        - Response: JSON response containing serialized data of the updated slot.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        - Http404: If the slot does not exist.
        """
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific slot.

        Parameters:
        - pk (int): The primary key of the slot.

        Returns:
        - Response: Empty response with status HTTP_204_NO_CONTENT.

        Raises:
        - Http404: If the slot does not exist.
        """
        slot = self.get_object(pk)
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
