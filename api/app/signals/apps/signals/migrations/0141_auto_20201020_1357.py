# Generated by Django 2.2.13 on 2020-10-20 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0140_signal_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='app',
            field=models.CharField(choices=[('MB', 'Mobiele Beheerder'), ('FC', 'Facilitator'), ('MCC', 'MyCleanCity'), ('SEDA', 'SEDA'), ('ESB', 'ESB')], default='SEDA', max_length=255),
        ),
    ]
