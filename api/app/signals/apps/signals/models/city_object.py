from django.contrib.gis.db import models
from signals.apps.signals.models.mixins import CreatedUpdatedModel


class CityObject(CreatedUpdatedModel):
    orac_comment = models.CharField(max_length=200, null=True, blank=True)
    oracCode = models.CharField(max_length=100)
    oracCategory = models.CharField(max_length=200, null=True, blank=True)
    oracType = models.CharField(max_length=200)

    def __str__(self):
        return self.oracCode
