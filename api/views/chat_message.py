from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.chat_message import ChatMessage
from api.serializers.chat_message import ChatMessageSerializer


class ChatMessageView(APIView):
    """
    API View to retrieve, create, update, or delete a chat message.
    """
    def get_object(self, pk):
        """
        Get a chat message object by its primary key.

        Parameters:
        - pk (int): The primary key of the chat message.

        Returns:
        - ChatMessage: The chat message object.

        Raises:
        - Http404: If the chat message with the given primary key does not exist.
        """
        try:
            return ChatMessage.objects.get(pk=pk)
        except ChatMessage.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a chat message.

        Parameters:
        - pk (int): The primary key of the chat message.

        Returns:
        - Response: Response containing the serialized data of the chat message.

        Raises:
        - status.HTTP_404_NOT_FOUND: If the chat message with the given primary key does not exist.
        """
        chat_message = self.get_object(pk)
        serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new chat message.

        Parameters:
        - request.data:
            - sender_id (int): The ID of the sender.
            - text (str): The text of the chat message.
            - chat_id (int): The ID of the chat.
            - time (str): The timestamp of the chat message.
            - diagnosis_id (optional, str): The ID of the associated diagnosis (if applicable).
            - appointment_id (optional, str): The ID of the associated appointment (if applicable).

        Returns:
        - Response: Response containing the serialized data of the created chat message.

        Raises:
        - status.HTTP_500_INTERNAL_SERVER_ERROR: If an error occurs while creating the chat message.
        """
        try:
            data = {}
            data['sender_id'] = int(request.data.get('sender_id'))
            data['text'] = request.data.get('text')
            data['chat_id'] = int(request.data.get('chat_id'))
            data['time'] = request.data.get('time')
            if request.data.get('diagnosis_id'):
                data['diagnosis_id'] = request.data.get('diagnosis_id')
            if request.data.get('appointment_id'):
                data['appointment_id'] = request.data.get('appointment_id')
            chat_message = ChatMessage.objects.create(**data)
            chat_message.save()
            return Response(ChatMessageSerializer(chat_message).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        """
        Update a chat message.

        Parameters:
        - request.data: The updated data of the chat message.

        Returns:
        - Response: Response containing the serialized data of the updated chat message.

        Raises:
        - status.HTTP_400_BAD_REQUEST: If the request data is invalid.
        """
        chat_message = self.get_object(pk)
        serializer = ChatMessageSerializer(chat_message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a chat message.

        Parameters:
        - pk (int): The primary key of the chat message.

        Returns:
        - Response: Empty response with status HTTP_204_NO_CONTENT.

        Raises:
        - status.HTTP_404_NOT_FOUND: If the chat message with the given primary key does not exist.
        """
        chat_message = self.get_object(pk)
        chat_message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
