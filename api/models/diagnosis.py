from django.db import models
from api.models.patient import Patient

class Diagnosis(models.Model):
    """
    Model representing a diagnosis.
    """

    image = models.ImageField(upload_to='media/diagnosis/%Y/%m/%d/')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dermatologist = models.ForeignKey('Dermatologist', on_delete=models.SET_NULL, null=True, default=None)
    extra_derm_info = models.TextField(max_length=500, null=True)
    approved = models.BooleanField(default=False)
    action = models.CharField(max_length=100, choices=[('Treatment', 'Treatment'), ('Referral', 'Referral'), ('Pending', 'Pending')], default='Pending')
    body_part = models.CharField(max_length=100)
    itchy = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the string representation of the diagnosis.
        """
        return str(self.id) + ' ' + str(self.image) + ' ' + str(self.patient) + ' ' + str(self.dermatologist) + ' ' + str(self.extra_derm_info) + ' ' + str(self.approved) + ' ' + str(self.action) + ' ' + str(self.body_part) + ' ' + str(self.itchy) + ' ' + str(self.date)
