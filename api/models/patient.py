from django.db import models
from django.contrib.auth.models import User

class Patient(User):
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])