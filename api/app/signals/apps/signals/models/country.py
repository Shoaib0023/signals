from django.contrib.gis.db import models

class Country(models.Model):
    country_id = models.CharField(max_length=255, null=True, blank=True)
    country_name = models.CharField(max_length=255)

    def __str__(self):
        ''' String representation of country '''
        return self.country_name

