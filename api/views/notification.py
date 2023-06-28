from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from api.models.notification import Notification
from api.serializers.notification import NotificationSerializer


class NotificationAPIView(APIView):
    """
    API View to retrieve, create, and update notifications.
    """

    def get(self, request):
        """
        Retrieve notifications for the authenticated user.

        Returns:
        - Response: JSON response containing serialized data of the user's notifications.
        """
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new notification for the authenticated user.

        Parameters:
        - request.data: JSON data containing the notification information.

        Returns:
        - Response: JSON response containing serialized data of the created notification.
        """
        data = request.data
        data['user'] = request.user.id
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing notification.

        Parameters:
        - pk (int): Primary key of the notification.
        - request.data: JSON data containing the updated notification information.

        Returns:
        - Response: JSON response containing serialized data of the updated notification.

        Raises:
        - status.HTTP_404_NOT_FOUND: If the notification does not exist.
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        """
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
