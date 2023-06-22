from django.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + str(self.latitude) + ' ' + str(self.longitude)