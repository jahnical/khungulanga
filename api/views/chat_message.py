from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.chat_message import ChatMessage
from api.serializers.chat_message import ChatMessageSerializer


class ChatMessageView(APIView):
    def get_object(self, pk):
        try:
            return ChatMessage.objects.get(pk=pk)
        except ChatMessage.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        chat_message = self.get_object(pk)
        serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            data = {}
            data['sender_id'] = int(request.data.get('sender_id'))
            data['text'] = request.data.get('text')
            data['chat_id'] = int(request.data.get('chat_id'))
            data['time'] = request.data.get('time')
            if (request.data.get('diagnosis_id')):
                data['diagnosis_id'] = request.data.get('diagnosis_id')
            if (request.data.get('appointment_id')):
                data['appointment_id'] = request.data.get('appointment_id')
            chat_message = ChatMessage.objects.create(**data)
            chat_message.save()
            print(data)
            return Response(ChatMessageSerializer(chat_message).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        chat_message = self.get_object(pk)
        serializer = ChatMessageSerializer(chat_message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        chat_message = self.get_object(pk)
        chat_message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
