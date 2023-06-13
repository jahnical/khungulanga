from django.db import models

class Slot(models.Model):
    start_time = models.TimeField()
    dermatologist = models.ForeignKey('Dermatologist', on_delete=models.CASCADE)
    scheduled = models.BooleanField(default=False)
    day_of_week = models.CharField(max_length=10)