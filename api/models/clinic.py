from django.db import models

class Clinic(models.Model):
    """
    Model representing a clinic.
    """

    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        """
        Returns the string representation of the clinic.
        """
        return str(self.id) + ' ' + self.name + ' ' + str(self.latitude) + ' ' + str(self.longitude)
