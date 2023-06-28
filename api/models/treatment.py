from django.db import models

class Treatment(models.Model):
    """
    Model representing a treatment for a disease.
    """

    disease = models.ForeignKey('Disease', on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        """
        Returns a string representation of the Treatment object.

        Format: <id> <disease> <description> <title>
        """
        return f"{self.id} {self.disease} {self.description} {self.title}"
