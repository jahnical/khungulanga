from django.db import models
from api.models.diagnosis import Diagnosis

from api.models.patient import Patient
from api.models.dermatologist import Dermatologist
from api.models.slot import Slot

class Appointment(models.Model):
    dermatologist = models.ForeignKey(Dermatologist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    book_date = models.DateField(null=True)
    appo_date = models.DateTimeField(null=True)
    done = models.BooleanField(default=False)
    duration = models.IntegerField(null=True)
    cost = models.FloatField(default=0.0)
    extra_info = models.TextField(max_length=1000, null=True)
    patient_removed = models.DateTimeField(null=True)
    dermatologist_removed = models.DateTimeField(null=True)
    patient_cancelled = models.DateTimeField(null=True)
    dermatologist_cancelled = models.DateTimeField(null=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + ' ' + self.patient.user.first_name + ' ' + self.dermatologist.user.first_name + ' ' + str(self.appo_date) + ' ' + str(self.done) + ' ' + str(self.duration) + ' ' + str(self.cost) + ' ' + str(self.extra_info) + ' ' + str(self.patient_removed) + ' ' + str(self.dermatologist_removed) + ' ' + str(self.patient_cancelled) + ' ' + str(self.dermatologist_cancelled) + ' ' + str(self.diagnosis) + ' ' + str(self.slot)