from django.contrib.gis.db import models
from signals.apps.signals.models.mixins import CreatedUpdatedModel


class SignalsActivity(CreatedUpdatedModel):
    activity_id = models.CharField(max_length=255)
    signal_id = models.ForeignKey('signals.Signal', on_delete=models.SET_NULL, null=True)
    to_app = models.CharField(max_length=255)
    from_app = models.CharField(max_length=255)
