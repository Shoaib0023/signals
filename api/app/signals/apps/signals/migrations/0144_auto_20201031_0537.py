# Generated by Django 2.2.13 on 2020-10-31 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0143_auto_20201029_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='descriptionId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='neighbourhood',
            name='descriptionId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
