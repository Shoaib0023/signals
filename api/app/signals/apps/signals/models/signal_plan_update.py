from django.contrib.gis.db import models
from signals.apps.signals.models.mixins import CreatedUpdatedModel


class SignalPlanUpdate(CreatedUpdatedModel):
    signal_id = models.CharField(max_length=255, null=False, blank=False)
    assign_to = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image =  models.FileField(
        upload_to='attachments/%Y/%m/%d/',
        null=True,
        blank=True,
        max_length=255
    )
