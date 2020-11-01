from django.contrib.gis.db import models
from signals.apps.signals.models.mixins import CreatedUpdatedModel


class SignalCityObject(CreatedUpdatedModel):
    complainID = models.CharField(max_length=200)
    complainIDall = models.CharField(max_length=200, null=True, blank=True)
    reportCount = models.CharField(max_length=200)
    city_obj = models.ForeignKey('signals.CityObject', null=True, blank=True, on_delete=models.SET_NULL)
    signal = models.ForeignKey('signals.Signal', null=True, blank=True, on_delete=models.SET_NULL)
    is_Orac = models.BooleanField(default=False)
