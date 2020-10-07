# Generated by Django 2.2.13 on 2020-09-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0129_auto_20200921_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='app',
            field=models.CharField(choices=[('MB', 'Mobile-Beherdeer'), ('FC', 'Facilitator'), ('MCC', 'MyCleanCity'), ('SEDA', 'SEDA')], default='SEDA', max_length=255),
        ),
    ]
