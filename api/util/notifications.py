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

def notify_appointment_booked(appointment):
    notification = NotificationModel.objects.create(
        user=appointment.dermatologist.user,
        title="Appointment Booked",
        message="You have a new appointment booked by " + appointment.patient.user.first_name + " " + appointment.patient.user.last_name + ".",
        route="appointment",
        related_id=appointment.id,
        related_name="Appointment"
    )
    notification.save()
    
    return send_notification(notification)

def notify_appointment_cancelled(appointment):
    cancelled_by = appointment.patient.user if appointment.patient_cancelled else appointment.dermatologist.user
    notify = appointment.dermatologist.user if appointment.patient_cancelled else appointment.patient.user
    notification = NotificationModel.objects.create(
        user=notify,
        title="Appointment Cancelled",
        message="Your appointment with " + cancelled_by.first_name + " " + cancelled_by.last_name + " has been cancelled.",
        route="appointment",
        related_id=appointment.id,
        related_name="Appointment"
    )
    notification.save()
    
    return send_notification(notification)