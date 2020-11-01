from django.contrib.gis.db import models

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    descriptionId = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        ''' String representation of District '''
        return f'{self.name} - {self.descriptionId}'

