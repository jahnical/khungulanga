from django.contrib.auth.models import User
from django.db import models

from api.models.clinic import Clinic

class Dermatologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.ImageField(upload_to='media/qualification/%Y/%m/%d/')
    specialization = models.CharField(max_length=100, default="DERMATOPATHOLOGIST", choices=[("COSMETIC", "Cosmetic Dermatologist"), ("DERMATOPATHOLOGIST", "Dermatopathologist"), ("DERMATOSURGEON", "Dermatosurgeon"), ("IMMUNODERMATOLOGIST", "Immunodermatologist"), ("MOHS_SURGEON", "Mohs Surgeon"), ("PAEDIATRIC", "Paediatric Dermatologist"), ("TELEDERMATOLOGIST", "Teledermatologist")])
    email = models.EmailField()
    phone_number = models.CharField(max_length=13)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    hourly_rate = models.FloatField()
    status = models.CharField(max_length=100, default="PENDING", choices=[("APPROVED", "Approved"), ("PENDING", "Pending"), ("REJECTED", "Rejected")])
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.user) + ' ' + str(self.qualification) + ' ' + str(self.specialization) + ' ' + str(self.email) + ' ' + str(self.phone_number) + ' ' + str(self.clinic) + ' ' + str(self.hourly_rate) + ' ' + str(self.status)