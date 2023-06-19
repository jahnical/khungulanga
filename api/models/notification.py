from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from api.serializers.user import UserSerializer

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)
    route = models.CharField(max_length=255)
    related_id = models.IntegerField(null=True)
    related_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'isRead': self.is_read,
            'route': self.route,
            'user_id': self.user.id,
            'related_id': self.related_id,
            'related_name': self.related_name,
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data['id'],
            title=json_data['title'],
            message=json_data['message'],
            timestamp=datetime.fromisoformat(json_data['timestamp']),
            is_read=json_data['isRead'],
            route=json_data['route'],
            user_id=json_data['user_id'],
            related_id=json_data['related_id'],
            related_name=json_data['related_name'],
        )