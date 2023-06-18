from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from api.models.notification import Notification
from asgiref.sync import async_to_sync

User = get_user_model()

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        notification_data = {
            'id': instance.id,
            'title': instance.title,
            'message': instance.message,
            'timestamp': instance.timestamp.isoformat(),
            'isRead': instance.is_read,
            'route': instance.route,
        }
