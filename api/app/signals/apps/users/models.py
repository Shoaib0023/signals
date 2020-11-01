from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from signals.apps.signals.models.mixins import CreatedUpdatedModel

User = get_user_model()


class Profile(CreatedUpdatedModel):
    """
    The profile model for a user
    """
    country = models.ForeignKey('signals.Country', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('signals.City', on_delete=models.SET_NULL, null=True)
    _type = models.CharField(max_length=100, null=True, blank=True)
    
    user = models.OneToOneField(
        to=User,
        related_name='profile',
        verbose_name=_('profile'),
        on_delete=models.CASCADE,
    )

    departments = models.ManyToManyField(
        to='signals.Department'
    )

    # SIG-2016 Added a note field to the profile
    note = models.TextField(null=True, blank=True)

    facilitator_role = models.CharField(max_length=255, null=True, blank=True)
    district = models.ForeignKey('signals.District', on_delete=models.SET_NULL, null=True)
    fac_user_id = models.CharField(max_length=255, blank=True, null=True)
    fac_district_id = models.CharField(max_length=255, blank=True, null=True)
    fac_neighbourhood_id  = models.CharField(max_length=255, blank=True, null=True)
    mb_district_id = models.CharField(max_length=255, blank=True, null=True)
    mb_neighbourhood_id = models.CharField(max_length=255, blank=True, null=True)
    mb_user_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
