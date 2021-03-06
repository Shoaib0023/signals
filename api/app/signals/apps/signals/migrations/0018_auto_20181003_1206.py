# Generated by Django 2.1.1 on 2018-10-03 10:06

from django.db import migrations


def remove_ip_address_in_existing_objects(apps, schema_editor):
    """Remove all ip addresses in existing objects for `Signal` and `Status`."""
    Signal = apps.get_model('signals', 'Signal')
    Status = apps.get_model('signals', 'Status')

    for signal in Signal.objects.all():
        try:
            del signal.extra_properties['IP']
        except (KeyError, TypeError):
            continue
        else:
            signal.save()
    for status in Status.objects.all():
        try:
            del status.extra_properties['IP']
        except (KeyError, TypeError):
            continue
        else:
            status.save()


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0017_auto_20181002_1111'),
    ]

    operations = [
        migrations.RunPython(remove_ip_address_in_existing_objects),
    ]
