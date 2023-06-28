from django.db import models

class Prediction(models.Model):
    """
    Model representing a prediction made for a diagnosis.
    """

    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, null=True)
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.CASCADE)
    probability = models.FloatField(default=0.0)
    approved = models.BooleanField(default=False)
    treatment = models.TextField(max_length=500, null=True)
    
    def __str__(self):
        """
        Returns a string representation of the Prediction object.

        Format: <id> <disease> <diagnosis> <probability> <approved> <treatment>
        """
        return f"{self.id} {self.disease} {self.diagnosis} {self.probability} {self.approved} {self.treatment}"
