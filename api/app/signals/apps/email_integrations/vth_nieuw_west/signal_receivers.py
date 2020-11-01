from django.dispatch import receiver

from signals.apps.email_integrations.vth_nieuw_west import tasks
from signals.apps.signals.managers import create_child, create_initial


@receiver(create_initial, dispatch_uid='vth_nieuw_west_email_create_initial')
def create_initial_handler(sender, signal_obj, **kwargs):
    tasks.send_mail_vth_nieuw_west.delay(pk=signal_obj.id)


@receiver(create_child, dispatch_uid='vth_nieuw_west_email_create_child')
def create_child_handler(sender, signal_obj, **kwargs):
    tasks.send_mail_vth_nieuw_west.delay(pk=signal_obj.id)
