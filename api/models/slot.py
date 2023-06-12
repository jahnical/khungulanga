from django.db import models

class Slot(models.Model):
    start_time = models.IntegerField()
    dermatologist = models.ForeignKey('Dermatologist', on_delete=models.CASCADE)
    scheduled = models.BooleanField(default=False)
    day_of_week = models.IntegerField(choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])