from django.contrib.gis.db import models

class PostCode(models.Model):
    post_code = models.CharField(max_length=100)
    stadsdeelId = models.ForeignKey('signals.District', related_name="postcode", on_delete=models.CASCADE)

    def __str__(self):
        ''' String representation of Neighbourhood '''
        return f'{self.name} - {self.descriptionId}'

