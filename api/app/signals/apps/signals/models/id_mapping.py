from django.contrib.gis.db import models

class IDMapping(models.Model):
    seda_signal_id = models.CharField(max_length=255, null=True, blank=True)
    mb_signal_id = models.CharField(max_length=255, null=True, blank=True)
    facilitator_signal_id = models.CharField(max_length=255, null=True, blank=True)
    mcc_signal_id = models.CharField(max_length=255, null=True, blank=True)
    web_form_id = models.CharField(max_length=255, null=True, blank=True)
    issue_final_image = models.FileField(
        upload_to='attachments/%Y/%m/%d/',
        null=True,
        blank=True,
        max_length=255
    )

    def __str__(self):
        return f'Seda ID - {self.seda_signal_id}, MB ID - {self.mb_signal_id}'
