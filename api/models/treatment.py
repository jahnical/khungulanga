from django.db import models

class Treatment(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.disease) + ' ' + self.description + ' ' + self.title