from django.http import HttpResponse
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message
from api.models.notification import Notification as NotificationModel

def send_notification(notification):
    """
    Send a notification to FCM devices.

    Args:
        notification (api.models.notification.Notification): The notification object.

    Returns:
        django.http.HttpResponse: The HTTP response indicating successful notification sending.

    """
    devices = FCMDevice.objects.filter(user=notification.user)

    print(devices.first())

    devices.send_message(Message(
        notification=Notification(
            title=notification.title,
            body=notification.message,
        ),
        data=notification.to_json()
    ))

    return HttpResponse('Notification sent successfully!')


def notify_diagnosis_to_confirm(diagnosis, dermatologist):
    """
    Notify a dermatologist about a new diagnosis to confirm.

    Args:
        diagnosis (api.models.diagnosis.Diagnosis): The diagnosis object.
        dermatologist (api.models.dermatologist.Dermatologist): The dermatologist object.

    Returns:
        django.http.HttpResponse: The HTTP response indicating successful notification sending.

    """
    notification = NotificationModel.objects.create(
        user=dermatologist.user,
        title="New diagnosis to confirm",
        message=f"{diagnosis.patient.user.first_name} {diagnosis.patient.user.last_name} has sent you a new diagnosis to confirm.",
        route="diagnosis",
        related_id=diagnosis.id,
        related_name="Diagnosis"
    )
    notification.save()

    return send_notification(notification)


def notify_diagnosis_feedback(diagnosis):
    """
    Notify a patient about feedback on their diagnosis.

    Args:
        diagnosis (api.models.diagnosis.Diagnosis): The diagnosis object.

    Returns:
        django.http.HttpResponse: The HTTP response indicating successful notification sending.

    """
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
    """
    Notify a dermatologist about a new appointment booked.

    Args:
        appointment (api.models.appointment.Appointment): The appointment object.

    Returns:
        django.http.HttpResponse: The HTTP response indicating successful notification sending.

    """
    notification = NotificationModel.objects.create(
        user=appointment.dermatologist.user,
        title="Appointment Booked",
        message=f"You have a new appointment booked by {appointment.patient.user.first_name} {appointment.patient.user.last_name}.",
        route="appointment",
        related_id=appointment.id,
        related_name="Appointment"
    )
    notification.save()

    return send_notification(notification)


def notify_appointment_cancelled(appointment, notify, cancelled_by):
    """
    Notify a user about an appointment being cancelled.

    Args:
        appointment (api.models.appointment.Appointment): The appointment object.
        notify (django.contrib.auth.models.User): The user to notify.
        cancelled_by (django.contrib.auth.models.User): The user who cancelled the appointment.

    Returns:
        django.http.HttpResponse: The HTTP response indicating successful notification sending.

    """
    notification = NotificationModel.objects.create(
        user=notify,
        title="Appointment Cancelled",
        message=f"Your appointment with {cancelled_by.first_name} {cancelled_by.last_name} has been cancelled.",
        route="appointment",
        related_id=appointment.id,
        related_name="Appointment"
    )
    notification.save()

    return send_notification(notification)


def notify_appointment_done(appointment, user_to_notify, user_marked):
    """
    Notify a user that their appointment has been marked as done.

    Args:
        appointment (api.models.appointment.Appointment): The appointment object.
        user_to_notify (django.contrib.auth.models.User): The user to notify.
        user_marked (django.contrib.auth.models.User): The user who marked the appointment as done.

    Returns:
        django.http.HttpResponse: The HTTP response indicating successful notification sending.

    """
    notification = NotificationModel.objects.create(
        user=user_to_notify,
        title="Appointment Done",
        message=f"Your appointment with {user_marked.first_name} {user_marked.last_name} has been marked as done.",
        route="appointment",
        related_id=appointment.id,
        related_name="Appointment"
    )
    notification.save()

    return send_notification(notification)
