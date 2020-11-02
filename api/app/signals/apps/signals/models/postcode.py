from django.contrib.gis.db import models

class PostCode(models.Model):
    post_code = models.CharField(max_length=100)
    stadsdeelId = models.ForeignKey('signals.District', related_name="postcode", on_delete=models.SET_NULL, null=True)
    neighbourhood = models.ForeignKey('signals.Neighbourhood', related_name="postcode", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        ''' String representation of Neighbourhood '''
        return f'{self.name} - {self.descriptionId}'
