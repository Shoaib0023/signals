# Generated by Django 2.2.13 on 2020-10-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0132_auto_20201004_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='signal',
            name='forman_emp_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='plan_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='report_days',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='urgency',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
