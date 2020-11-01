from django.contrib.gis.db import models

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100, unique=True)
    descriptionId = models.CharField(max_length=100, blank=True, null=True)
    district = models.ForeignKey('signals.District', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        ''' String representation of Neighbourhood '''
        return f'{self.name} - {self.descriptionId}'

