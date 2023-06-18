from rest_framework import serializers
from api.models.notification import Notification

class NotificationSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'timestamp', 'is_read', 'route', 'related_id', 'related_name']
