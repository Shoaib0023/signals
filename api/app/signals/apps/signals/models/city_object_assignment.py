from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

from signals.apps.signals.models.mixins import CreatedUpdatedModel


class CityObjectAssignment(CreatedUpdatedModel):
    """Many-to-Many through model for `Signal` <-> `CityObject`."""
    _signal = models.ForeignKey('signals.Signal',
                                on_delete=models.CASCADE,
                                related_name='city_object_assignments')
    city_object = models.ForeignKey('signals.CityObject',
                                 on_delete=models.CASCADE,
                                 related_name='city_object_assignments')
    created_by = models.EmailField(null=True, blank=True)

    def __str__(self):
        """String representation."""
        return '{cityObject} - {signal}'.format(cityObject=self.city_object, signal=self._signal)
