from django.db import models

class Prediction(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, null=True)
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.CASCADE)
    probability = models.FloatField(default=0.0)
    approved = models.BooleanField(default=False)
    treatment = models.TextField(max_length=500, null=True)
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.disease) + ' ' + str(self.diagnosis) + ' ' + str(self.probability) + ' ' + str(self.approved) + ' ' + str(self.treatment)