from django.contrib.gis.db import models
from signals.apps.signals.models.mixins import CreatedUpdatedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class SignalsPlan(CreatedUpdatedModel):
    report_id = models.ForeignKey('signals.Signal', related_name="reports" ,on_delete=models.CASCADE)
    emp_id = models.ForeignKey('signals.Reporter', related_name="signals", on_delete=models.SET_NULL, null=True)
    report_days = models.CharField(max_length=100)
    report_date = models.DateField()
    report_time = models.TimeField()
    forman_email = models.EmailField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
