from django.contrib.gis.db import models
from signals.apps.signals.models.mixins import CreatedUpdatedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class SignalsPlan(CreatedUpdatedModel):
    signal = models.ForeignKey('signals.Signal', related_name="reports", on_delete=models.SET_NULL, null=True)
    reporter = models.ForeignKey('signals.Reporter', related_name="signals", on_delete=models.SET_NULL, null=True)
    report_days = models.CharField(max_length=100)
    schedule_datetime = models.DateTimeField(null=True, blank=True)
    forman_email = models.EmailField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
