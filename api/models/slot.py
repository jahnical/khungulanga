from django.db import models

class Slot(models.Model):
    """
    Model representing a time slot for a dermatologist's availability.
    """

    start_time = models.TimeField()
    dermatologist = models.ForeignKey('Dermatologist', on_delete=models.CASCADE)
    scheduled = models.BooleanField(default=False)
    day_of_week = models.CharField(max_length=10)
    
    def __str__(self):
        """
        Returns a string representation of the Slot object.

        Format: <id> <start_time> <dermatologist> <scheduled> <day_of_week>
        """
        return f"{self.id} {self.start_time} {self.dermatologist} {self.scheduled} {self.day_of_week}"
