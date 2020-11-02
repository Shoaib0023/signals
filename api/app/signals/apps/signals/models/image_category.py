from django.contrib.gis.db import models


class ImageCategory(models.Model):
    category_level_name1 = models.CharField(max_length=255, null=True, blank=True)
    category_level_name2 = models.CharField(max_length=255, null=True, blank=True)
    category_level_name3 = models.CharField(max_length=255, null=True, blank=True)
    category_level_name4 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.category_level_name1} - {self.category_level_name2} - {self.category_level_name3} - {self.category_level_name4}'
