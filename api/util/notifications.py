from django.http import HttpResponse
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message
from api.models.notification import Notification as NotificationModel

def send_notification(notification):
    # Retrieve FCM tokens of target devices
    devices = FCMDevice.objects.filter(user=notification.user)
    
    print(devices.first())

    # Send notification to devices
    devices.send_message(Message(
        notification=Notification(
            title=notification.title,
            body=notification.message,
        ),
        data=notification.to_json()
    ))

    return HttpResponse('Notification sent successfully!')

def notify_diagnosis_to_confirm(diagnosis, dermatologist):
    notification = NotificationModel.objects.create(
        user=dermatologist.user,
        title="New diagnosis to confirm",
        message= diagnosis.patient.user.first_name + " " + diagnosis.patient.user.last_name + " has sent you a new diagnosis to confirm.",
        route="diagnosis",
        related_id=diagnosis.id,
        related_name="Diagnosis"
    )
    notification.save()
    
    return send_notification(notification)

def notify_diagnosis_feedback(diagnosis):
    notification = NotificationModel.objects.create(
        user=diagnosis.patient.user,
        title="Diagnosis Feedback",
        message="You have received feedback on your diagnosis",
        route="diagnosis",
        related_id=diagnosis.id,
        related_name="Diagnosis"
    )
    notification.save()
    
    return send_notification(notification)