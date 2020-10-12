from django.contrib.gis.db import models

class District(models.Model):
    name = models.CharField(max_length=100)
    descriptionId = models.CharField(max_length=100)

    def __str__(self):
        ''' String representation of District '''
        return f'{self.name} - {self.descriptionId}'

