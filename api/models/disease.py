from django.db import models

class Disease(models.Model):
    """
    Model representing a disease.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    severity = models.IntegerField(choices=[(1, "Mild"), (2, "Moderate"), (3, "Severe")])

    def __str__(self):
        """
        Returns the string representation of the disease.
        """
        return str(self.id) + ' ' + self.name + ' ' + self.description + ' ' + str(self.severity)
