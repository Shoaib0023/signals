from django.contrib.gis.db import models

class City(models.Model):
    city_id = models.CharField(max_length=255, null=True, blank=True)
    city_name = models.CharField(max_length=255)

    def __str__(self):
        ''' String representation of country '''
        return self.city_name

