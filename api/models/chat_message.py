from django.db import models
from django.contrib.auth.models import User
from api.models.appointment import Appointment
from api.models.appointment_chat import AppointmentChat
from api.models.diagnosis import Diagnosis

class ChatMessage(models.Model):
    """
    Model representing a chat message.
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    chat = models.ForeignKey(AppointmentChat, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        """
        Returns the string representation of the chat message.
        """
        return str(self.id) + ' ' + str(self.sender) + ' ' + self.text + ' ' + str(self.chat) + ' ' + str(self.diagnosis) + ' ' + str(self.appointment) + ' ' + str(self.time) + ' ' + str(self.seen)
