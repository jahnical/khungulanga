from django.db import models
from api.models.patient import Patient
class Diagnosis(models.Model):
    image = models.ImageField(upload_to='media/diagnosis/%Y/%m/%d/')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dermatologist = models.ForeignKey('Dermatologist', on_delete=models.SET_NULL, null=True, default=None)
    extra_derm_info = models.TextField(max_length=500, null=True)
    approved = models.BooleanField(default=False)
    action = models.CharField(max_length=100, choices=[('Treatment', 'Treatment'), ('Referral', 'Referral'), ('Pending', 'Pending')], default='Pending')
    body_part = models.CharField(max_length=100)
    itchy = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
