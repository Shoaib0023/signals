from django.contrib.gis.db import models

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)
    descriptionId = models.CharField(max_length=100)

    def __str__(self):
        ''' String representation of Neighbourhood '''
        return f'{self.name} - {self.descriptionId}'

