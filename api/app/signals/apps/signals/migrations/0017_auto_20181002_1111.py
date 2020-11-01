# Generated by Django 2.1.1 on 2018-10-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0016_auto_20180927_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='state',
            field=models.CharField(blank=True, choices=[
                ('m', 'Gemeld'), ('i', 'In afwachting van behandeling'),
                ('b', 'In behandeling'),
                ('h', 'On hold'),
                ('ready to send', 'Te verzenden naar extern systeem'),
                ('o', 'Afgehandeld'),
                ('a', 'Geannuleerd'),
                ('sent', 'Verzonden naar extern systeem'),
                ('send failed', 'Verzending naar extern systeem mislukt'),
                ('done external', 'Melding is afgehandeld in extern systeem')
            ], default='m', help_text='Melding status', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='target_api',
            field=models.CharField(blank=True,
                                   choices=[('sigmax', 'Sigmax (City Control)')],
                                   max_length=250,
                                   null=True),
        ),
    ]
